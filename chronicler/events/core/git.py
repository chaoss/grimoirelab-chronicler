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

from typing import Any

from cloudevents.http import CloudEvent

from ...eventizer import Eventizer, uuid


GIT_EVENT_COMMIT = "org.grimoirelab.events.git.commit"
GIT_EVENT_MERGE_COMMIT = "org.grimoirelab.events.git.merge"
GIT_EVENT_ACTION_ADDED = "org.grimoirelab.events.git.file.added"
GIT_EVENT_ACTION_MODIFIED = "org.grimoirelab.events.git.file.modified"
GIT_EVENT_ACTION_DELETED = "org.grimoirelab.events.git.file.deleted"
GIT_EVENT_ACTION_REPLACED = "org.grimoirelab.events.git.file.replaced"
GIT_EVENT_ACTION_COPIED = "org.grimoirelab.events.git.file.copied"
GIT_EVENT_ACTION_TYPE_CHANGED = "org.grimoirelab.events.git.file.typechanged"


class GitEventizer(Eventizer):
    """Eventize git commits"""

    def eventize_item(self, raw_item: dict[str, Any]) -> list[dict[str, Any]]:
        events = []

        item_uuid = raw_item.get('uuid', None)

        if not item_uuid:
            raise ValueError("'uuid' attribute not found on item.")
        if raw_item['backend_name'].lower() != 'git':
            raise ValueError(f"Item {item_uuid} is not a 'git' item.")
        if raw_item['category'] != 'commit':
            raise ValueError(f"Invalid category '{raw_item['category']}' for '{item_uuid}' item.")

        if 'Merge' in raw_item['data']:
            event_type = GIT_EVENT_MERGE_COMMIT
        else:
            event_type = GIT_EVENT_COMMIT

        attributes = {
            "id": item_uuid,
            "type": event_type,
            "source": raw_item['origin'],
            "time": raw_item['updated_on'],
        }

        event = CloudEvent(attributes, raw_item['data'])
        events.append(event)

        action_events = self._eventize_commit_actions(event,
                                                      raw_item['data']['files'])

        events.extend(action_events)

        return events

    def _eventize_commit_actions(self, parent_event: CloudEvent, raw_files_data):

        events = []

        for file_data in raw_files_data:
            actions = file_data.get('action', None)

            if not actions and parent_event['type'] == GIT_EVENT_COMMIT:
                raise ValueError(f"No action for commit event {parent_event['id']}")
            elif not actions:
                continue

            if parent_event['type'] == GIT_EVENT_COMMIT:
                action_event = self._process_action(parent_event['source'],
                                                    parent_event['time'],
                                                    parent_event['id'], actions, file_data)
                events.append(action_event)
            else:
                prev_merge_action = None
                for action in actions:
                    if action == prev_merge_action:
                        continue

                    action_event = self._process_action(parent_event['source'],
                                                        parent_event['time'],
                                                        parent_event['id'], action, file_data)
                    events.append(action_event)
                    prev_merge_action = action
        return events

    def _process_action(self, source, time, event_uuid, action, file_data):
        if action == 'A':
            event_type = GIT_EVENT_ACTION_ADDED
        elif action == 'M':
            event_type = GIT_EVENT_ACTION_MODIFIED
        elif action == 'D':
            event_type = GIT_EVENT_ACTION_DELETED
        elif action.startswith('R'):
            event_type = GIT_EVENT_ACTION_REPLACED
        elif action.startswith('C'):
            event_type = GIT_EVENT_ACTION_COPIED
        elif action.startswith('T'):
            event_type = GIT_EVENT_ACTION_TYPE_CHANGED
        else:
            raise ValueError(f"No valid action: {action}")

        id_args = [event_uuid, file_data['file'], action]
        if 'newfile' in file_data:
            id_args.append(file_data['newfile'])

        event_id = uuid(*id_args)

        data = {
            "filename": file_data['file'],
            "modes": file_data['modes'],
            "indexes": file_data['indexes'],
            "similarity": action[1:] if action in ('R', 'C') else None,
            "new_filename": file_data.get('newfile', None),
            "added_lines": file_data.get('added', None),
            "deleted_lines": file_data.get('removed', None)
        }

        attributes = {
            "id": event_id,
            "linked_event": event_uuid,
            "type": event_type,
            "source": source,
            "time": time,
        }

        event = CloudEvent(attributes, data)

        return event
