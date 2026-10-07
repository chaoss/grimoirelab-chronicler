# -*- coding: utf-8 -*-
#
# Copyright (C) GrimoireLab Developers
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import logging

from typing import Any, Optional

from cloudevents.http import CloudEvent

from grimoirelab_toolkit.datetime import str_to_datetime
from grimoirelab_toolkit.identities import generate_uuid

from ...eventizer import Eventizer, uuid


GITHUB_DATASOURCE = "github"

GITHUB_EVENT_ISSUE = "org.grimoirelab.events.github.issue"
GITHUB_EVENT_PULL_REQUEST = "org.grimoirelab.events.github.pull_request"
GITHUB_EVENT_COMMENT = "org.grimoirelab.events.github.comment"

GITHUB_EVENT_AUTHOR = "org.grimoirelab.events.github.author"
GITHUB_EVENT_ASSIGNEE = "org.grimoirelab.events.github.assignee"
GITHUB_EVENT_CLOSED_BY = "org.grimoirelab.events.github.closed_by"
GITHUB_EVENT_CREATED_BY = "org.grimoirelab.events.github.created_by"
GITHUB_EVENT_COMMENT_AUTHOR = "org.grimoirelab.events.github.comment.author"

ISSUE_IDENTITY_TYPES = {
    "user": GITHUB_EVENT_AUTHOR,
    "assignee": GITHUB_EVENT_ASSIGNEE,
    "assignees": GITHUB_EVENT_ASSIGNEE,
    "closed_by": GITHUB_EVENT_CLOSED_BY,
    "created_by": GITHUB_EVENT_CREATED_BY,
}

COMMENT_IDENTITY_TYPES = {
    "user": GITHUB_EVENT_COMMENT_AUTHOR,
}


logger = logging.getLogger(__name__)


class GitHubEventizer(Eventizer):
    """Eventize GitHub issues and pull requests."""

    def eventize_item(self, raw_item: dict[str, Any]) -> list[CloudEvent]:
        events = []

        item_uuid = raw_item.get("uuid", None)

        if not item_uuid:
            raise ValueError("'uuid' attribute not found on item.")
        if raw_item["backend_name"].lower() != GITHUB_DATASOURCE:
            raise ValueError(f"Item {item_uuid} is not a {GITHUB_DATASOURCE} item.")
        if raw_item["category"] not in ("issue", "pull_request"):
            raise ValueError(f"Invalid category '{raw_item['category']}' for '{item_uuid}' item.")

        if "pull_request" in raw_item["data"]:
            event_type = GITHUB_EVENT_PULL_REQUEST
        else:
            event_type = GITHUB_EVENT_ISSUE

        attributes = {
            "id": item_uuid,
            "type": event_type,
            "source": raw_item["origin"],
            "time": raw_item["updated_on"],
        }

        # Remove all URL fields from the event data that are not needed
        event_data = self._strip_url_fields(raw_item["data"])

        cloud_event = CloudEvent(attributes, event_data)
        events.append(cloud_event)

        comment_events = self._eventize_comments(cloud_event, event_data)
        events.extend(comment_events)

        identities_events = self._eventize_identities(cloud_event, event_data, ISSUE_IDENTITY_TYPES)
        events.extend(identities_events)

        return events

    def _strip_url_fields(self, obj):
        """Recursively remove all fields ending with '_url' from the given object.

        :param obj: Object to strip URL fields from

        :returns: Object without URL fields
        """
        if isinstance(obj, dict):
            return {
                key: self._strip_url_fields(value)
                for key, value in obj.items()
                if "_url" not in key
            }

        if isinstance(obj, list):
            return [self._strip_url_fields(item) for item in obj]

        return obj

    def _eventize_comments(
        self, parent_event: CloudEvent, raw_data: dict[str, Any]
    ) -> list[CloudEvent]:
        """Eventize comments from a GitHub issue or pull request item."""

        events = []

        comments = raw_data.get("comments_data", [])
        for comment in comments:
            comment_id = comment.get("id", None)
            if not comment_id:
                logger.warning(f"Comment without 'id' in item '{parent_event['id']}'. Skipping.")
                continue

            event_id = uuid(parent_event["id"], GITHUB_EVENT_COMMENT, str(comment_id))

            comment["issue_number"] = raw_data["number"]

            time = str_to_datetime(comment["updated_at"]).timestamp()

            attributes = {
                "id": event_id,
                "linked_event": parent_event["id"],
                "type": GITHUB_EVENT_COMMENT,
                "source": parent_event["source"],
                "time": time,
            }

            cloud_event = CloudEvent(attributes, comment)
            events.append(cloud_event)

            identities_events = self._eventize_identities(
                cloud_event, comment, COMMENT_IDENTITY_TYPES
            )
            events.extend(identities_events)

        return events

    def _eventize_identities(
        self,
        parent_event: CloudEvent,
        raw_item: dict[str, Any],
        identity_types: dict[str, Any],
    ) -> list[CloudEvent]:
        """Eventize issue identities from a GitHub issue item."""

        events = []

        for identity_type, event_type in identity_types.items():
            # In _data we have the full user data
            identity_attr = identity_type + "_data"

            identity_data = raw_item.get(identity_attr, None)
            if not identity_data:
                continue

            if isinstance(identity_data, list):
                for item in identity_data:
                    user = self._process_identity(
                        parent_event=parent_event,
                        raw_identity=item,
                        event_type=event_type,
                    )
                    if user:
                        events.append(user)
            else:
                user = self._process_identity(
                    parent_event=parent_event,
                    raw_identity=identity_data,
                    event_type=event_type,
                )
                if user:
                    events.append(user)
        return events

    def _process_identity(
        self,
        parent_event: CloudEvent,
        raw_identity: dict[str, Any],
        event_type: str,
    ) -> Optional[CloudEvent]:
        """Obtain a CloudEvent for a given identity.

        :param parent_event: Parent CloudEvent
        :param raw_identity: Raw identity data from the item
        :param event_type: Type of identity event

        :returns: CloudEvent for the identity
        """
        source = parent_event["source"]
        time = parent_event["time"]
        parent_id = parent_event["id"]

        identity = {
            "username": raw_identity.get("login"),
            "email": raw_identity.get("email", None),
            "name": raw_identity.get("name", None),
        }
        try:
            identity_id = generate_uuid(
                source=GITHUB_DATASOURCE,
                email=identity["email"],
                name=identity["name"],
                username=identity["username"],
            )
        except ValueError as e:
            logger.warning(
                f"Cannot generate UUID for identity '{raw_identity}' "
                f"in event '{parent_id}': {e}. Skipping."
            )
            return None

        event_id = uuid(parent_id, event_type, identity_id)

        data = {
            "source": GITHUB_DATASOURCE,
            "name": identity["name"],
            "username": identity["username"],
            "email": identity["email"],
            "uuid": identity_id,
        }
        attributes = {
            "id": event_id,
            "linked_event": parent_id,
            "type": event_type,
            "source": source,
            "time": time,
        }

        return CloudEvent(attributes, data)
