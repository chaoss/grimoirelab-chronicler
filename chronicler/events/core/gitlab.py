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

from grimoirelab_toolkit.identities import generate_uuid

from ...eventizer import Eventizer, uuid


GITLAB_DATASOURCE = "gitlab"

GITLAB_EVENT_ISSUE = "org.grimoirelab.events.gitlab.issue"

GITLAB_EVENT_AUTHOR = "org.grimoirelab.events.gitlab.author"
GITLAB_EVENT_ASSIGNEE = "org.grimoirelab.events.gitlab.assignee"
GITLAB_EVENT_CLOSED_BY = "org.grimoirelab.events.gitlab.closed_by"

ISSUE_IDENTITY_TYPES = {
    "author": GITLAB_EVENT_AUTHOR,
    "assignees": GITLAB_EVENT_ASSIGNEE,
    "closed_by": GITLAB_EVENT_CLOSED_BY,
}

logger = logging.getLogger(__name__)


class GitLabEventizer(Eventizer):
    """Eventize GitLab issues and merge requests.

    The incoming `raw_item` is expected to be a chronicler item produced by
    Perceval/driver for GitLab. Field names can vary, so the implementation is
    defensive and tries common variants (for example: 'notes' or
    'comments_data' for comments, 'iid' or 'number' for the issue number).
    """

    def eventize_item(self, raw_item: dict[str, Any]) -> list[CloudEvent]:
        events: list[CloudEvent] = []

        item_uuid = raw_item.get("uuid")
        if not item_uuid:
            raise ValueError("'uuid' attribute not found on item.")
        if raw_item["backend_name"].lower() != GITLAB_DATASOURCE:
            raise ValueError(f"Item {item_uuid} is not a {GITLAB_DATASOURCE} item.")

        category = raw_item.get("category")
        if category == "issue":
            event_type = GITLAB_EVENT_ISSUE
        else:
            raise ValueError(f"Unsupported category '{category}' for item '{item_uuid}'.")

        attributes = {
            "id": item_uuid,
            "type": event_type,
            "source": raw_item["origin"],
            "time": raw_item["updated_on"],
        }

        cloud_event = CloudEvent(attributes, raw_item["data"])
        events.append(cloud_event)

        identities_events = self._eventize_identities(
            cloud_event, raw_item["data"], ISSUE_IDENTITY_TYPES
        )
        events.extend(identities_events)

        return events

    def _eventize_identities(
        self,
        parent_event: CloudEvent,
        raw_item: dict[str, Any],
        identity_types: dict[str, Any],
    ) -> list[CloudEvent]:
        """Eventize issue identities from a GitLab issue item."""

        events: list[CloudEvent] = []

        for identity_type, event_type in identity_types.items():
            identity_data = raw_item.get(identity_type)
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
            "username": raw_identity.get("username"),
            "email": raw_identity.get("public_email") or None,
            "name": raw_identity.get("name") or None,
        }

        try:
            identity_id = generate_uuid(
                source=GITLAB_DATASOURCE,
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
            "source": GITLAB_DATASOURCE,
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
