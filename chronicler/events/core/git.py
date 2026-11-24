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
import re
from collections.abc import Generator
from typing import Any

from cloudevents.http import CloudEvent
from grimoirelab_toolkit.identities import generate_uuid

from ...eventizer import Eventizer, Identity, uuid
from .events import (
    Commit,
    CommitAckedBy,
    CommitAuthoredBy,
    CommitCoAuthoredBy,
    CommitCommittedBy,
    CommitFileAdded,
    CommitFileCopied,
    CommitFileDeleted,
    CommitFileModified,
    CommitFileReplaced,
    CommitFileTypeChanged,
    CommitHelpedBy,
    CommitMentoredBy,
    CommitReportedBy,
    CommitReviewedBy,
    CommitSignedOffBy,
    CommitSuggestedBy,
    CommitTestedBy,
    IdentityEvent,
    MergeCommit,
)

GIT_DATASOURCE = "git"

# Names of the commit fields on Perceval items and
# the generic ones used by the commit events.
GIT_COMMIT_FIELDS = {
    "Author": "author",
    "AuthorDate": "author_date",
    "Commit": "committer",
    "CommitDate": "commit_date",
    "Merge": "merge",
}

COMMIT_TRAILERS = {
    "Acked-by": CommitAckedBy,
    "Co-authored-by": CommitCoAuthoredBy,
    "Helped-by": CommitHelpedBy,
    "Mentored-by": CommitMentoredBy,
    "Reported-by": CommitReportedBy,
    "Reviewed-by": CommitReviewedBy,
    "Signed-off-by": CommitSignedOffBy,
    "Suggested-by": CommitSuggestedBy,
    "Tested-by": CommitTestedBy,
}

# Pair programming regex. Some matching examples are:
#   - John Smith, John Doe and Jane Rae <pairprogramming@example.com>
#   - John Smith, John Doe & Jane Rae <pairprogramming@example>
#   - John Smith and John Doe <pairpogramming@example>
GIT_AUTHORS_REGEX = re.compile(
    r"(?P<first_authors>.+?)\s+(?:[aA][nN][dD]|&|\+)\s+(?P<last_author>.+?)\s+<(?P<email>[^>]+)>"
)

logger = logging.getLogger(__name__)


class GitEventizer(Eventizer):
    """Eventize git commits"""

    def eventize_item(self, raw_item: dict[str, Any]) -> list[CloudEvent]:
        events = []

        item_uuid = raw_item.get("uuid", None)

        if not item_uuid:
            raise ValueError("'uuid' attribute not found on item.")
        if raw_item["backend_name"].lower() != GIT_DATASOURCE:
            raise ValueError(f"Item {item_uuid} is not a '{GIT_DATASOURCE}' item.")
        if raw_item["category"] != "commit":
            raise ValueError(f"Invalid category '{raw_item['category']}' for '{item_uuid}' item.")

        if "Merge" in raw_item["data"]:
            event_class = MergeCommit
        else:
            event_class = Commit

        data = {GIT_COMMIT_FIELDS.get(k, k): v for k, v in raw_item["data"].items()}

        # Fields that are not part of the event definition, such as
        # the trailers, are kept in the data of the event.
        names = {f.name for f in event_class.data_fields()} - {"extra"}
        commit_data = {k: v for k, v in data.items() if k in names}
        extra = {k: v for k, v in data.items() if k not in names}

        event = event_class(
            id=item_uuid,
            source=raw_item["origin"],
            datasource=GIT_DATASOURCE,
            time=raw_item["updated_on"],
            extra=extra,
            **commit_data,
        ).to_cloudevent()
        events.append(event)

        action_events = self._eventize_commit_actions(
            event, raw_item["data"]["commit"], raw_item["data"]["files"]
        )

        events.extend(action_events)

        identities_events = self._eventize_commit_identities(event, raw_item)

        events.extend(identities_events)

        return events

    def _eventize_commit_actions(
        self,
        parent_event: CloudEvent,
        commit_hash: str,
        raw_files_data: list[dict[str, Any]],
    ) -> list[CloudEvent]:
        events = []

        for file_data in raw_files_data:
            actions = file_data.get("action", None)

            if not actions and parent_event["type"] == Commit.TYPE:
                raise ValueError(f"No action for commit event {parent_event['id']}")
            elif not actions:
                continue

            if parent_event["type"] == Commit.TYPE:
                action_event = self._process_action(
                    parent_event["source"],
                    parent_event["time"],
                    parent_event["id"],
                    commit_hash,
                    actions,
                    file_data,
                )
                events.append(action_event)
            else:
                prev_merge_action = None
                for action in actions:
                    if action == prev_merge_action:
                        continue

                    action_event = self._process_action(
                        parent_event["source"],
                        parent_event["time"],
                        parent_event["id"],
                        commit_hash,
                        action,
                        file_data,
                    )
                    events.append(action_event)
                    prev_merge_action = action
        return events

    def _process_action(
        self,
        source: str,
        time: float,
        event_uuid: str,
        commit_hash: str,
        action: str,
        file_data: dict[str, Any],
    ) -> CloudEvent:
        if action == "A":
            event_class = CommitFileAdded
        elif action == "M":
            event_class = CommitFileModified
        elif action == "D":
            event_class = CommitFileDeleted
        elif action.startswith("R"):
            event_class = CommitFileReplaced
        elif action.startswith("C"):
            event_class = CommitFileCopied
        elif action.startswith("T"):
            event_class = CommitFileTypeChanged
        else:
            raise ValueError(f"No valid action: {action}")

        id_args = [event_uuid, file_data["file"], action]
        if "newfile" in file_data:
            id_args.append(file_data["newfile"])

        event_id = uuid(*id_args)

        event = event_class(
            id=event_id,
            linkedevent=event_uuid,
            source=source,
            datasource=GIT_DATASOURCE,
            time=time,
            commit=commit_hash,
            filename=file_data["file"],
            modes=file_data["modes"],
            indexes=file_data["indexes"],
            similarity=action[1:] if action in ("R", "C") else None,
            new_filename=file_data.get("newfile", None),
            added_lines=file_data.get("added", None),
            deleted_lines=file_data.get("removed", None),
        )

        return event.to_cloudevent()

    def _eventize_commit_identities(
        self,
        parent_event: CloudEvent,
        raw_item: dict[str, Any],
    ) -> list[CloudEvent]:
        """Eventize commit identities from a git commit item."""

        events = []

        authors = self._parse_authors(raw_item["data"]["Author"])
        identity_events = self._process_identities(
            parent_event["source"],
            parent_event["time"],
            parent_event["id"],
            CommitAuthoredBy,
            authors,
        )
        events.extend(identity_events)

        committers = self._parse_authors(raw_item["data"]["Commit"])
        identity_events = self._process_identities(
            parent_event["source"],
            parent_event["time"],
            parent_event["id"],
            CommitCommittedBy,
            committers,
        )
        events.extend(identity_events)

        for trailer, event_class in COMMIT_TRAILERS.items():
            signers = raw_item["data"].get(trailer, [])
            identity_events = self._process_identities(
                parent_event["source"],
                parent_event["time"],
                parent_event["id"],
                event_class,
                signers,
            )
            events.extend(identity_events)

        return events

    def _process_identities(
        self,
        source: str,
        time: str,
        event_uuid: str,
        event_class: type[IdentityEvent],
        raw_identities: list[str],
    ) -> Generator[CloudEvent, None, None]:
        """Obtain identity events from a list of identities.

        :param source: source of the event
        :param time: time of the event
        :param event_uuid: UUID of the parent event
        :param event_class: class of the identity event
        :param raw_identities: list of strings with the identities information

        :returns: generator of CloudEvent with the identity information
        """
        for raw_identity in raw_identities:
            try:
                identity = self._parse_identity(raw_identity)
                identity_id = generate_uuid(
                    source=GIT_DATASOURCE,
                    email=identity.email,
                    name=identity.name,
                    username=identity.username,
                )
            except ValueError as e:
                logger.warning(
                    f"Cannot generate UUID for identity '{raw_identity}' "
                    f"in event '{event_uuid}': {e}. Skipping."
                )
                continue

            role = event_class.TYPE.split(".")[-1]
            event_id = uuid(event_uuid, role, identity_id)

            event = event_class(
                id=event_id,
                linkedevent=event_uuid,
                source=source,
                datasource=GIT_DATASOURCE,
                time=time,
                name=identity.name,
                username=identity.username,
                email=identity.email,
                uuid=identity_id,
            )

            yield event.to_cloudevent()

    @staticmethod
    def _parse_authors(authors: str) -> list[str]:
        """Parse a list of authors from a string."""

        m = GIT_AUTHORS_REGEX.match(authors)
        if m:
            authors = m.group("first_authors").split(",")
            authors = [author.strip() for author in authors]
            authors += [m.group("last_author")]
            authors += [f"<{m.group('email')}>"]
            return authors
        else:
            return [authors]

    @staticmethod
    def _parse_identity(git_author: str) -> Identity:
        """Extract identity information from a Git author string."""

        fields = git_author.split("<")
        name = fields[0]
        name = name.strip()
        if not name:
            name = None
        email = None
        if len(fields) > 1:
            email = git_author.split("<")[1][:-1]

        return Identity(email=email, name=name)
