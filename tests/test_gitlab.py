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

import json
import unittest

from chronicler.events.core.gitlab import (
    GitLabEventizer,
    GITLAB_EVENT_ISSUE,
    GITLAB_EVENT_ASSIGNEE,
    GITLAB_EVENT_AUTHOR,
)


class GitLabEventizerTestCase(unittest.TestCase):
    """Unit tests for GitLabEventizer class"""

    def test_eventize_item_issue(self):
        """Check if it produces the right events from an issue"""

        eventizer = GitLabEventizer()

        raw_item = {
            "backend_name": "GitLab",
            "backend_version": "1.0.0",
            "category": "issue",
            "classified_fields_filtered": None,
            "data": {
                "_links": {
                    "award_emoji": "https://gitlab.com/api/v4/projects/77837443/issues/1/award_emoji",
                    "closed_as_duplicate_of": None,
                    "notes": "https://gitlab.com/api/v4/projects/77837443/issues/1/notes",
                    "project": "https://gitlab.com/api/v4/projects/77837443",
                    "self": "https://gitlab.com/api/v4/projects/77837443/issues/1",
                },
                "assignee": {
                    "avatar_url": "https://secure.gravatar.com/avatar/xxxx?s=80&d=identicon",
                    "id": 8276902,
                    "locked": False,
                    "name": "User Test",
                    "public_email": "",
                    "state": "active",
                    "username": "user_1",
                    "web_url": "https://gitlab.com/user_1",
                },
                "assignees": [
                    {
                        "avatar_url": "https://secure.gravatar.com/avatar/xxxx?s=80&d=identicon",
                        "id": 8276902,
                        "locked": False,
                        "name": "User Test",
                        "public_email": "",
                        "state": "active",
                        "username": "user_1",
                        "web_url": "https://gitlab.com/user_1",
                    }
                ],
                "author": {
                    "avatar_url": "https://secure.gravatar.com/avatar/xxxx?s=80&d=identicon",
                    "id": 8276902,
                    "locked": False,
                    "name": "User Test",
                    "public_email": "",
                    "state": "active",
                    "username": "user_1",
                    "web_url": "https://gitlab.com/user_1",
                },
                "award_emoji_data": [],
                "blocking_issues_count": 0,
                "closed_at": None,
                "closed_by": None,
                "confidential": False,
                "created_at": "2026-01-20T09:55:57.188Z",
                "description": "Body issue 1",
                "discussion_locked": None,
                "downvotes": 0,
                "due_date": None,
                "has_tasks": True,
                "id": 181476619,
                "iid": 1,
                "imported": False,
                "imported_from": "none",
                "issue_type": "issue",
                "labels": [],
                "merge_requests_count": 0,
                "milestone": None,
                "moved_to_id": None,
                "notes_data": [
                    {
                        "author": {
                            "avatar_url": "https://secure.gravatar.com/avatar/xxxx?s=80&d=identicon",
                            "id": 8276902,
                            "locked": False,
                            "name": "User Test",
                            "public_email": "",
                            "state": "active",
                            "username": "user_1",
                            "web_url": "https://gitlab.com/user_1",
                        },
                        "award_emoji_data": [],
                        "body": "assigned to @user_1",
                        "commands_changes": {},
                        "confidential": False,
                        "created_at": "2026-01-20T09:55:57.529Z",
                        "id": 3019317146,
                        "imported": False,
                        "imported_from": "none",
                        "internal": False,
                        "noteable_id": 181476619,
                        "noteable_iid": 1,
                        "noteable_type": "Issue",
                        "project_id": 77837443,
                        "resolvable": False,
                        "system": True,
                        "type": None,
                        "updated_at": "2026-01-20T09:55:57.536Z",
                    },
                    {
                        "author": {
                            "avatar_url": "https://secure.gravatar.com/avatar/xxxx?s=80&d=identicon",
                            "id": 8276902,
                            "locked": False,
                            "name": "User Test",
                            "public_email": "",
                            "state": "active",
                            "username": "user_1",
                            "web_url": "https://gitlab.com/user_1",
                        },
                        "award_emoji_data": [],
                        "body": "This is a comment",
                        "commands_changes": {},
                        "confidential": False,
                        "created_at": "2026-01-20T10:18:14.789Z",
                        "id": 3019389027,
                        "imported": False,
                        "imported_from": "none",
                        "internal": False,
                        "noteable_id": 181476619,
                        "noteable_iid": 1,
                        "noteable_type": "Issue",
                        "project_id": 77837443,
                        "resolvable": False,
                        "system": False,
                        "type": None,
                        "updated_at": "2026-01-20T10:18:14.789Z",
                    },
                ],
                "project_id": 77837443,
                "references": {"full": "user_1/tmp#1", "relative": "#1", "short": "#1"},
                "service_desk_reply_to": None,
                "severity": "UNKNOWN",
                "state": "opened",
                "task_completion_status": {"completed_count": 0, "count": 0},
                "task_status": "0 of 0 checklist items completed",
                "time_stats": {
                    "human_time_estimate": None,
                    "human_total_time_spent": None,
                    "time_estimate": 0,
                    "total_time_spent": 0,
                },
                "title": "Example issue 1",
                "type": "ISSUE",
                "updated_at": "2026-01-20T10:18:14.879Z",
                "upvotes": 0,
                "user_notes_count": 1,
                "web_url": "https://gitlab.com/user_1/tmp/-/issues/1",
            },
            "origin": "https://gitlab.com/user_1/tmp",
            "perceval_version": "1.4.4",
            "search_fields": {
                "groups": None,
                "iid": 1,
                "item_id": "181476619",
                "owner": "user_1",
                "project": "tmp",
            },
            "tag": "https://gitlab.com/user_1/tmp",
            "timestamp": 1768904308.924827,
            "updated_on": 1768904294.879,
            "uuid": "753f641525292d18618695f3c4ea7d36a9253fce",
        }

        events = eventizer.eventize_item(raw_item)

        self.assertEqual(len(events), 3)

        issue_event = events[0]
        self.assertEqual(issue_event["id"], "753f641525292d18618695f3c4ea7d36a9253fce")
        self.assertEqual(issue_event["type"], GITLAB_EVENT_ISSUE)
        self.assertEqual(issue_event["source"], "https://gitlab.com/user_1/tmp")
        self.assertEqual(issue_event["time"], 1768904294.879)
        self.assertEqual(issue_event.data["web_url"], "https://gitlab.com/user_1/tmp/-/issues/1")

        action_event = events[1]
        self.assertEqual(action_event["id"], "4c7134547d2f6d4dbdb8231222e35606095db45e")
        self.assertEqual(action_event["linked_event"], "753f641525292d18618695f3c4ea7d36a9253fce")
        self.assertEqual(action_event["type"], GITLAB_EVENT_AUTHOR)
        self.assertEqual(issue_event["source"], "https://gitlab.com/user_1/tmp")
        self.assertEqual(action_event["time"], 1768904294.879)
        self.assertEqual(action_event.data["source"], "gitlab")
        self.assertEqual(action_event.data["username"], "user_1")
        self.assertEqual(action_event.data["name"], "User Test")
        self.assertIsNone(action_event.data["email"])
        self.assertEqual(action_event.data["uuid"], "a98c43afe5107a8b8a98e4bf00306fb2c5453481")

        action_event = events[2]
        self.assertEqual(action_event["id"], "16015c50f2e11af6cc2c8bfcf5df4494abd1b1e0")
        self.assertEqual(action_event["linked_event"], "753f641525292d18618695f3c4ea7d36a9253fce")
        self.assertEqual(action_event["type"], GITLAB_EVENT_ASSIGNEE)
        self.assertEqual(issue_event["source"], "https://gitlab.com/user_1/tmp")
        self.assertEqual(action_event["time"], 1768904294.879)
        self.assertEqual(action_event.data["source"], "gitlab")
        self.assertEqual(action_event.data["username"], "user_1")
        self.assertEqual(action_event.data["name"], "User Test")
        self.assertIsNone(action_event.data["email"])
        self.assertEqual(action_event.data["uuid"], "a98c43afe5107a8b8a98e4bf00306fb2c5453481")

    def test_eventize(self):
        """Check if eventizes a full set of items"""

        eventizer = GitLabEventizer()

        with open("data/gitlab_issues.txt", "r") as file:
            issues = [json.loads(line.strip()) for line in file.readlines()]

        events = list(eventizer.eventize(issues))
        self.assertEqual(len(events), 11)

    def test_eventize_item_invalid_backend(self):
        """Check invalid backend item type"""

        eventizer = GitLabEventizer()

        raw_item = {
            "uuid": "1234",
            "backend_name": "git",
            "category": "issue",
            "origin": "repo1",
            "updated_on": 1392185439.0,
            "data": {"files": []},
        }
        with self.assertRaises(ValueError) as context:
            _ = eventizer.eventize_item(raw_item)
        self.assertEqual(str(context.exception), "Item 1234 is not a gitlab item.")

    def test_eventize_item_invalid_category(self):
        """Check invalid backend item category"""

        eventizer = GitLabEventizer()

        raw_item = {
            "uuid": "1234",
            "backend_name": "GitLab",
            "category": "commit",
            "origin": "repo1",
            "updated_on": 1392185439.0,
            "data": {"files": []},
        }
        with self.assertRaises(ValueError) as context:
            _ = eventizer.eventize_item(raw_item)
        self.assertEqual(str(context.exception), "Unsupported category 'commit' for item '1234'.")

    def test_eventize_item_no_uuid(self):
        """Check invalid backend item category"""

        eventizer = GitLabEventizer()

        raw_item = {
            "backend_name": "GitLab",
            "category": "issue",
            "origin": "repo1",
            "updated_on": 1392185439.0,
            "data": {"files": []},
        }
        with self.assertRaises(ValueError) as context:
            _ = eventizer.eventize_item(raw_item)
        self.assertEqual(str(context.exception), "'uuid' attribute not found on item.")


if __name__ == "__main__":
    unittest.main()
