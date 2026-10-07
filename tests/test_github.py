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

from chronicler.events.core.github import (
    GitHubEventizer,
    GITHUB_EVENT_ISSUE,
    GITHUB_EVENT_COMMENT,
    GITHUB_EVENT_AUTHOR,
    GITHUB_EVENT_ASSIGNEE,
    GITHUB_EVENT_COMMENT_AUTHOR,
)


class GitHubEventizerTestCase(unittest.TestCase):
    """Unit tests for GitHubEventizer class"""

    def test_eventize_item_issue(self):
        """Check if it produces the right events from a issue"""

        eventizer = GitHubEventizer()

        raw_item = {
            "backend_name": "GitHub",
            "backend_version": "1.0.0",
            "perceval_version": "1.4.0",
            "timestamp": 1.768822194040383e9,
            "origin": "https://github.com/user_1/tmp",
            "uuid": "a548ead04e53ace59cbfc271849b23d00dc9d251",
            "updated_on": 1.768819573e9,
            "classified_fields_filtered": None,
            "category": "issue",
            "search_fields": {
                "item_id": "3829113706",
                "owner": "user_1",
                "repo": "tmp",
            },
            "tag": "https://github.com/user_1/tmp",
            "data": {
                "url": "https://api.github.com/repos/user_1/tmp/issues/1",
                "repository_url": "https://api.github.com/repos/user_1/tmp",
                "labels_url": "https://api.github.com/repos/user_1/tmp/issues/1/labels{/name}",
                "comments_url": "https://api.github.com/repos/user_1/tmp/issues/1/comments",
                "events_url": "https://api.github.com/repos/user_1/tmp/issues/1/events",
                "html_url": "https://github.com/user_1/tmp/issues/1",
                "id": 3829113706,
                "node_id": "I_kwDOLc5Lw87kO6Nq",
                "number": 1,
                "title": "Test issue",
                "user": {
                    "login": "user_1",
                    "id": 51320071,
                    "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                    "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/user_1",
                    "html_url": "https://github.com/user_1",
                    "followers_url": "https://api.github.com/users/user_1/followers",
                    "following_url": "https://api.github.com/users/user_1/following{/other_user}",
                    "gists_url": "https://api.github.com/users/user_1/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/user_1/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/user_1/subscriptions",
                    "organizations_url": "https://api.github.com/users/user_1/orgs",
                    "repos_url": "https://api.github.com/users/user_1/repos",
                    "events_url": "https://api.github.com/users/user_1/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/user_1/received_events",
                    "type": "User",
                    "user_view_type": "public",
                    "site_admin": False,
                },
                "labels": [
                    {
                        "id": 6658949253,
                        "node_id": "LA_kwDOLc5Lw88AAAABjOeAhQ",
                        "url": "https://api.github.com/repos/user_1/tmp/labels/bug",
                        "name": "bug",
                        "color": "d73a4a",
                        "default": True,
                        "description": "Something isn't working",
                    }
                ],
                "state": "open",
                "locked": False,
                "assignee": None,
                "assignees": [],
                "milestone": None,
                "comments": 0,
                "created_at": "2026-01-19T10:45:53Z",
                "updated_at": "2026-01-19T10:46:13Z",
                "closed_at": None,
                "author_association": "OWNER",
                "active_lock_reason": None,
                "sub_issues_summary": {
                    "total": 0,
                    "completed": 0,
                    "percent_completed": 0,
                },
                "issue_dependencies_summary": {
                    "blocked_by": 0,
                    "total_blocked_by": 0,
                    "blocking": 0,
                    "total_blocking": 0,
                },
                "body": "Description issue",
                "closed_by": {
                    "login": "user_1",
                    "id": 51320071,
                    "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                    "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/user_1",
                    "html_url": "https://github.com/user_1",
                    "followers_url": "https://api.github.com/users/user_1/followers",
                    "following_url": "https://api.github.com/users/user_1/following{/other_user}",
                    "gists_url": "https://api.github.com/users/user_1/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/user_1/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/user_1/subscriptions",
                    "organizations_url": "https://api.github.com/users/user_1/orgs",
                    "repos_url": "https://api.github.com/users/user_1/repos",
                    "events_url": "https://api.github.com/users/user_1/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/user_1/received_events",
                    "type": "User",
                    "user_view_type": "public",
                    "site_admin": False,
                },
                "reactions": {
                    "url": "https://api.github.com/repos/user_1/tmp/issues/1/reactions",
                    "total_count": 0,
                    "+1": 0,
                    "-1": 0,
                    "laugh": 0,
                    "hooray": 0,
                    "confused": 0,
                    "heart": 0,
                    "rocket": 0,
                    "eyes": 0,
                },
                "timeline_url": "https://api.github.com/repos/user_1/tmp/issues/1/timeline",
                "performed_via_github_app": None,
                "state_reason": "reopened",
                "user_data": {
                    "login": "user_1",
                    "id": 51320071,
                    "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                    "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/user_1",
                    "html_url": "https://github.com/user_1",
                    "followers_url": "https://api.github.com/users/user_1/followers",
                    "following_url": "https://api.github.com/users/user_1/following{/other_user}",
                    "gists_url": "https://api.github.com/users/user_1/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/user_1/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/user_1/subscriptions",
                    "organizations_url": "https://api.github.com/users/user_1/orgs",
                    "repos_url": "https://api.github.com/users/user_1/repos",
                    "events_url": "https://api.github.com/users/user_1/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/user_1/received_events",
                    "type": "User",
                    "user_view_type": "public",
                    "site_admin": False,
                    "name": None,
                    "company": None,
                    "blog": "",
                    "location": None,
                    "email": None,
                    "hireable": None,
                    "bio": None,
                    "twitter_username": None,
                    "public_repos": 14,
                    "public_gists": 0,
                    "followers": 0,
                    "following": 0,
                    "created_at": "2019-06-03T09:54:17Z",
                    "updated_at": "2026-01-19T10:45:12Z",
                    "organizations": [],
                },
                "assignee_data": None,
                "assignees_data": [],
                "comments_data": [],
                "reactions_data": [],
            },
        }

        events = eventizer.eventize_item(raw_item)

        self.assertEqual(len(events), 2)

        issue_event = events[0]
        self.assertEqual(issue_event["id"], "a548ead04e53ace59cbfc271849b23d00dc9d251")
        self.assertEqual(issue_event["type"], GITHUB_EVENT_ISSUE)
        self.assertEqual(issue_event["source"], "https://github.com/user_1/tmp")
        self.assertEqual(issue_event["time"], 1768819573.0)
        self.assertEqual(
            issue_event.data["url"], "https://api.github.com/repos/user_1/tmp/issues/1"
        )

        action_event = events[1]
        self.assertEqual(action_event["id"], "a2f65d33ea545741a01d279372db7fddf69677d5")
        self.assertEqual(action_event["linked_event"], "a548ead04e53ace59cbfc271849b23d00dc9d251")
        self.assertEqual(action_event["type"], GITHUB_EVENT_AUTHOR)
        self.assertEqual(issue_event["source"], "https://github.com/user_1/tmp")
        self.assertEqual(action_event["time"], 1768819573.0)
        self.assertEqual(action_event.data["source"], "github")
        self.assertEqual(action_event.data["username"], "user_1")
        self.assertIsNone(action_event.data["name"])
        self.assertIsNone(action_event.data["email"])
        self.assertEqual(action_event.data["uuid"], "aa534061d6bbf5897a03b6508d519cb7af1215c4")

    def test_eventize(self):
        """Check if eventizes a full set of items"""

        eventizer = GitHubEventizer()

        with open("data/github_issues.txt", "r") as file:
            issues = [json.loads(line.strip()) for line in file.readlines()]

        events = list(eventizer.eventize(issues))
        self.assertEqual(len(events), 16)

    def test_eventize_item_invalid_backend(self):
        """Check invalid backend item type"""

        eventizer = GitHubEventizer()

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
        self.assertEqual(str(context.exception), "Item 1234 is not a github item.")

    def test_eventize_item_invalid_category(self):
        """Check invalid backend item category"""

        eventizer = GitHubEventizer()

        raw_item = {
            "uuid": "1234",
            "backend_name": "GitHub",
            "category": "commit",
            "origin": "repo1",
            "updated_on": 1392185439.0,
            "data": {"files": []},
        }
        with self.assertRaises(ValueError) as context:
            _ = eventizer.eventize_item(raw_item)
        self.assertEqual(str(context.exception), "Invalid category 'commit' for '1234' item.")

    def test_eventize_item_no_uuid(self):
        """Check invalid backend item category"""

        eventizer = GitHubEventizer()

        raw_item = {
            "backend_name": "GitHub",
            "category": "issue",
            "origin": "repo1",
            "updated_on": 1392185439.0,
            "data": {"files": []},
        }
        with self.assertRaises(ValueError) as context:
            _ = eventizer.eventize_item(raw_item)
        self.assertEqual(str(context.exception), "'uuid' attribute not found on item.")

    def test_eventize_comments(self):
        """Check if events with comments are generated correctly"""

        eventizer = GitHubEventizer()

        raw_item = {
            "backend_name": "GitHub",
            "backend_version": "1.0.0",
            "perceval_version": "1.4.0",
            "timestamp": 1768825308.844442,
            "origin": "https://github.com/example_user/tmp",
            "uuid": "a548ead04e53ace59cbfc271849b23d00dc9d251",
            "updated_on": 1768819573.0,
            "classified_fields_filtered": None,
            "category": "issue",
            "search_fields": {
                "item_id": "3829113706",
                "owner": "example_user",
                "repo": "tmp",
            },
            "tag": "https://github.com/example_user/tmp",
            "data": {
                "url": "https://api.github.com/repos/example_user/tmp/issues/1",
                "repository_url": "https://api.github.com/repos/example_user/tmp",
                "labels_url": "https://api.github.com/repos/example_user/tmp/issues/1/labels{/name}",
                "comments_url": "https://api.github.com/repos/example_user/tmp/issues/1/comments",
                "events_url": "https://api.github.com/repos/example_user/tmp/issues/1/events",
                "html_url": "https://github.com/example_user/tmp/issues/1",
                "id": 3829113706,
                "node_id": "I_kwDOLc5Lw87kO6Nq",
                "number": 1,
                "title": "Test issue",
                "user": {
                    "login": "example_user",
                    "id": 51320071,
                    "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                    "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/example_user",
                    "html_url": "https://github.com/example_user",
                    "followers_url": "https://api.github.com/users/example_user/followers",
                    "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                    "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                    "organizations_url": "https://api.github.com/users/example_user/orgs",
                    "repos_url": "https://api.github.com/users/example_user/repos",
                    "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/example_user/received_events",
                    "type": "User",
                    "user_view_type": "public",
                    "site_admin": False,
                },
                "labels": [
                    {
                        "id": 6658949253,
                        "node_id": "LA_kwDOLc5Lw88AAAABjOeAhQ",
                        "url": "https://api.github.com/repos/example_user/tmp/labels/bug",
                        "name": "bug",
                        "color": "d73a4a",
                        "default": True,
                        "description": "Something isn't working",
                    }
                ],
                "state": "open",
                "locked": False,
                "assignee": {
                    "login": "example_user",
                    "id": 51320071,
                    "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                    "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/example_user",
                    "html_url": "https://github.com/example_user",
                    "followers_url": "https://api.github.com/users/example_user/followers",
                    "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                    "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                    "organizations_url": "https://api.github.com/users/example_user/orgs",
                    "repos_url": "https://api.github.com/users/example_user/repos",
                    "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/example_user/received_events",
                    "type": "User",
                    "user_view_type": "public",
                    "site_admin": False,
                },
                "assignees": [
                    {
                        "login": "example_user",
                        "id": 51320071,
                        "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                        "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                        "gravatar_id": "",
                        "url": "https://api.github.com/users/example_user",
                        "html_url": "https://github.com/example_user",
                        "followers_url": "https://api.github.com/users/example_user/followers",
                        "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                        "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                        "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                        "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                        "organizations_url": "https://api.github.com/users/example_user/orgs",
                        "repos_url": "https://api.github.com/users/example_user/repos",
                        "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                        "received_events_url": "https://api.github.com/users/example_user/received_vents",
                        "type": "User",
                        "user_view_type": "public",
                        "site_admin": False,
                    }
                ],
                "milestone": None,
                "comments": 1,
                "created_at": "2026-01-19T10:45:53Z",
                "updated_at": "2026-01-19T10:46:13Z",
                "closed_at": None,
                "author_association": "OWNER",
                "active_lock_reason": None,
                "sub_issues_summary": {
                    "total": 0,
                    "completed": 0,
                    "percent_completed": 0,
                },
                "issue_dependencies_summary": {
                    "blocked_by": 0,
                    "total_blocked_by": 0,
                    "blocking": 0,
                    "total_blocking": 0,
                },
                "body": "Description issue",
                "closed_by": {
                    "login": "example_user",
                    "id": 51320071,
                    "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                    "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/example_user",
                    "html_url": "https://github.com/example_user",
                    "followers_url": "https://api.github.com/users/example_user/followers",
                    "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                    "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                    "organizations_url": "https://api.github.com/users/example_user/orgs",
                    "repos_url": "https://api.github.com/users/example_user/repos",
                    "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/example_user/received_events",
                    "type": "User",
                    "user_view_type": "public",
                    "site_admin": False,
                },
                "reactions": {
                    "url": "https://api.github.com/repos/example_user/tmp/issues/1/reactions",
                    "total_count": 0,
                    "+1": 0,
                    "-1": 0,
                    "laugh": 0,
                    "hooray": 0,
                    "confused": 0,
                    "heart": 0,
                    "rocket": 0,
                    "eyes": 0,
                },
                "timeline_url": "https://api.github.com/repos/example_user/tmp/issues/1/timeline",
                "performed_via_github_app": None,
                "state_reason": "reopened",
                "user_data": {
                    "login": "example_user",
                    "id": 51320071,
                    "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                    "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/example_user",
                    "html_url": "https://github.com/example_user",
                    "followers_url": "https://api.github.com/users/example_user/followers",
                    "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                    "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                    "organizations_url": "https://api.github.com/users/example_user/orgs",
                    "repos_url": "https://api.github.com/users/example_user/repos",
                    "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/example_user/received_events",
                    "type": "User",
                    "user_view_type": "public",
                    "site_admin": False,
                    "name": None,
                    "company": None,
                    "blog": "",
                    "location": None,
                    "email": None,
                    "hireable": None,
                    "bio": None,
                    "twitter_username": None,
                    "public_repos": 14,
                    "public_gists": 0,
                    "followers": 0,
                    "following": 0,
                    "created_at": "2019-06-03T09:54:17Z",
                    "updated_at": "2026-01-19T10:45:12Z",
                    "organizations": [],
                },
                "assignee_data": {
                    "login": "example_user",
                    "id": 51320071,
                    "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                    "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/example_user",
                    "html_url": "https://github.com/example_user",
                    "followers_url": "https://api.github.com/users/example_user/followers",
                    "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                    "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                    "organizations_url": "https://api.github.com/users/example_user/orgs",
                    "repos_url": "https://api.github.com/users/example_user/repos",
                    "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/example_user/received_events",
                    "type": "User",
                    "user_view_type": "public",
                    "site_admin": False,
                    "name": None,
                    "company": None,
                    "blog": "",
                    "location": None,
                    "email": None,
                    "hireable": None,
                    "bio": None,
                    "twitter_username": None,
                    "public_repos": 14,
                    "public_gists": 0,
                    "followers": 0,
                    "following": 0,
                    "created_at": "2019-06-03T09:54:17Z",
                    "updated_at": "2026-01-19T10:45:12Z",
                    "organizations": [],
                },
                "assignees_data": [
                    {
                        "login": "example_user",
                        "id": 51320071,
                        "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                        "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                        "gravatar_id": "",
                        "url": "https://api.github.com/users/example_user",
                        "html_url": "https://github.com/example_user",
                        "followers_url": "https://api.github.com/users/example_user/followers",
                        "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                        "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                        "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                        "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                        "organizations_url": "https://api.github.com/users/example_user/orgs",
                        "repos_url": "https://api.github.com/users/example_user/repos",
                        "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                        "received_events_url": "https://api.github.com/users/example_user/received_events",
                        "type": "User",
                        "user_view_type": "public",
                        "site_admin": False,
                        "name": None,
                        "company": None,
                        "blog": "",
                        "location": None,
                        "email": None,
                        "hireable": None,
                        "bio": None,
                        "twitter_username": None,
                        "public_repos": 14,
                        "public_gists": 0,
                        "followers": 0,
                        "following": 0,
                        "created_at": "2019-06-03T09:54:17Z",
                        "updated_at": "2026-01-19T10:45:12Z",
                        "organizations": [],
                    }
                ],
                "comments_data": [
                    {
                        "url": "https://api.github.com/repos/example_user/tmp/issues/comments/3767671300",
                        "html_url": "https://github.com/example_user/tmp/issues/1#issuecomment-3767671300",
                        "issue_url": "https://api.github.com/repos/example_user/tmp/issues/1",
                        "id": 3767671300,
                        "node_id": "IC_kwDOLc5Lw87gkhoE",
                        "user": {
                            "login": "example_user",
                            "id": 51320071,
                            "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                            "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                            "gravatar_id": "",
                            "url": "https://api.github.com/users/example_user",
                            "html_url": "https://github.com/example_user",
                            "followers_url": "https://api.github.com/users/example_user/followers",
                            "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                            "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                            "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                            "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                            "organizations_url": "https://api.github.com/users/example_user/orgs",
                            "repos_url": "https://api.github.com/users/example_user/repos",
                            "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                            "received_events_url": "https://api.github.com/users/example_user/received_events",
                            "type": "User",
                            "user_view_type": "public",
                            "site_admin": False,
                        },
                        "created_at": "2026-01-19T10:45:59Z",
                        "updated_at": "2026-01-19T10:45:59Z",
                        "body": "Comment 1",
                        "author_association": "OWNER",
                        "reactions": {
                            "url": "https://api.github.com/repos/example_user/tmp/issues/comments/3767671300/reactions",
                            "total_count": 1,
                            "+1": 1,
                            "-1": 0,
                            "laugh": 0,
                            "hooray": 0,
                            "confused": 0,
                            "heart": 0,
                            "rocket": 0,
                            "eyes": 0,
                        },
                        "performed_via_github_app": None,
                        "user_data": {
                            "login": "example_user",
                            "id": 51320071,
                            "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                            "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                            "gravatar_id": "",
                            "url": "https://api.github.com/users/example_user",
                            "html_url": "https://github.com/example_user",
                            "followers_url": "https://api.github.com/users/example_user/followers",
                            "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                            "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                            "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                            "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                            "organizations_url": "https://api.github.com/users/example_user/orgs",
                            "repos_url": "https://api.github.com/users/example_user/repos",
                            "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                            "received_events_url": "https://api.github.com/users/example_user/received_events",
                            "type": "User",
                            "user_view_type": "public",
                            "site_admin": False,
                            "name": None,
                            "company": None,
                            "blog": "",
                            "location": None,
                            "email": None,
                            "hireable": None,
                            "bio": None,
                            "twitter_username": None,
                            "public_repos": 14,
                            "public_gists": 0,
                            "followers": 0,
                            "following": 0,
                            "created_at": "2019-06-03T09:54:17Z",
                            "updated_at": "2026-01-19T10:45:12Z",
                            "organizations": [],
                        },
                        "reactions_data": [
                            {
                                "id": 324746517,
                                "node_id": "REA_lALOLc5Lw87gkhoEzhNbPRU",
                                "user": {
                                    "login": "example_user",
                                    "id": 51320071,
                                    "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                                    "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                                    "gravatar_id": "",
                                    "url": "https://api.github.com/users/example_user",
                                    "html_url": "https://github.com/example_user",
                                    "followers_url": "https://api.github.com/users/example_user/followers",
                                    "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                                    "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                                    "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                                    "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                                    "organizations_url": "https://api.github.com/users/example_user/orgs",
                                    "repos_url": "https://api.github.com/users/example_user/repos",
                                    "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                                    "received_events_url": "https://api.github.com/users/example_user/received_events",
                                    "type": "User",
                                    "user_view_type": "public",
                                    "site_admin": False,
                                },
                                "content": "+1",
                                "created_at": "2026-01-19T10:46:01Z",
                                "user_data": {
                                    "login": "example_user",
                                    "id": 51320071,
                                    "node_id": "MDQ6VXNlcjUxMzIwMDcx",
                                    "avatar_url": "https://avatars.githubusercontent.com/u/51320071?v=4",
                                    "gravatar_id": "",
                                    "url": "https://api.github.com/users/example_user",
                                    "html_url": "https://github.com/example_user",
                                    "followers_url": "https://api.github.com/users/example_user/followers",
                                    "following_url": "https://api.github.com/users/example_user/following{/other_user}",
                                    "gists_url": "https://api.github.com/users/example_user/gists{/gist_id}",
                                    "starred_url": "https://api.github.com/users/example_user/starred{/owner}{/repo}",
                                    "subscriptions_url": "https://api.github.com/users/example_user/subscriptions",
                                    "organizations_url": "https://api.github.com/users/example_user/orgs",
                                    "repos_url": "https://api.github.com/users/example_user/repos",
                                    "events_url": "https://api.github.com/users/example_user/events{/privacy}",
                                    "received_events_url": "https://api.github.com/users/example_user/received_events",
                                    "type": "User",
                                    "user_view_type": "public",
                                    "site_admin": False,
                                    "name": None,
                                    "company": None,
                                    "blog": "",
                                    "location": None,
                                    "email": None,
                                    "hireable": None,
                                    "bio": None,
                                    "twitter_username": None,
                                    "public_repos": 14,
                                    "public_gists": 0,
                                    "followers": 0,
                                    "following": 0,
                                    "created_at": "2019-06-03T09:54:17Z",
                                    "updated_at": "2026-01-19T10:45:12Z",
                                    "organizations": [],
                                },
                            }
                        ],
                    }
                ],
                "reactions_data": [],
            },
        }

        events = eventizer.eventize_item(raw_item)

        self.assertEqual(len(events), 6)

        issue_event = events[0]
        self.assertEqual(issue_event["id"], "a548ead04e53ace59cbfc271849b23d00dc9d251")
        self.assertEqual(issue_event["type"], GITHUB_EVENT_ISSUE)
        self.assertEqual(issue_event["source"], "https://github.com/example_user/tmp")
        self.assertEqual(issue_event["time"], 1768819573.0)
        self.assertEqual(
            issue_event.data["url"],
            "https://api.github.com/repos/example_user/tmp/issues/1",
        )
        self.assertEqual(issue_event.data["title"], "Test issue")

        action_event = events[1]
        self.assertEqual(action_event["id"], "c4ca608a321600f4353fcf6265838d30ac23e67c")
        self.assertEqual(action_event["linked_event"], "a548ead04e53ace59cbfc271849b23d00dc9d251")
        self.assertEqual(action_event["type"], GITHUB_EVENT_COMMENT)
        self.assertEqual(action_event["source"], "https://github.com/example_user/tmp")
        self.assertEqual(action_event["time"], 1768819559.0)
        self.assertEqual(
            action_event.data["url"],
            "https://api.github.com/repos/example_user/tmp/issues/comments/3767671300",
        )
        self.assertEqual(action_event.data["body"], "Comment 1")

        action_event = events[2]
        self.assertEqual(action_event["id"], "f5e97ba626a64961846512f4024c42cd802179e3")
        self.assertEqual(action_event["linked_event"], "c4ca608a321600f4353fcf6265838d30ac23e67c")
        self.assertEqual(action_event["type"], GITHUB_EVENT_COMMENT_AUTHOR)
        self.assertEqual(action_event["source"], "https://github.com/example_user/tmp")
        self.assertEqual(action_event["time"], 1768819559.0)
        self.assertEqual(action_event.data["source"], "github")
        self.assertEqual(action_event.data["username"], "example_user")
        self.assertIsNone(action_event.data["name"])
        self.assertIsNone(action_event.data["email"])
        self.assertEqual(action_event.data["uuid"], "b93094c8f58be3d61ba4d9e19a1603a18ce0e758")

        action_event = events[3]
        self.assertEqual(action_event["id"], "f2f4bc38d02975f2fc0553ec4def64b7be49bfbb")
        self.assertEqual(action_event["linked_event"], "a548ead04e53ace59cbfc271849b23d00dc9d251")
        self.assertEqual(action_event["type"], GITHUB_EVENT_AUTHOR)
        self.assertEqual(action_event["source"], "https://github.com/example_user/tmp")
        self.assertEqual(action_event["time"], 1768819573.0)
        self.assertEqual(action_event.data["source"], "github")
        self.assertEqual(action_event.data["username"], "example_user")
        self.assertIsNone(action_event.data["name"])
        self.assertIsNone(action_event.data["email"])
        self.assertEqual(action_event.data["uuid"], "b93094c8f58be3d61ba4d9e19a1603a18ce0e758")

        action_event = events[4]
        self.assertEqual(action_event["id"], "7c2a2b2bfe9625cd69654942612c8b1e47ab55e7")
        self.assertEqual(action_event["linked_event"], "a548ead04e53ace59cbfc271849b23d00dc9d251")
        self.assertEqual(action_event["type"], GITHUB_EVENT_ASSIGNEE)
        self.assertEqual(action_event["source"], "https://github.com/example_user/tmp")
        self.assertEqual(action_event["time"], 1768819573.0)
        self.assertEqual(action_event.data["source"], "github")
        self.assertEqual(action_event.data["username"], "example_user")
        self.assertIsNone(action_event.data["name"])
        self.assertIsNone(action_event.data["email"])
        self.assertEqual(action_event.data["uuid"], "b93094c8f58be3d61ba4d9e19a1603a18ce0e758")

        action_event = events[5]
        self.assertEqual(action_event["id"], "7c2a2b2bfe9625cd69654942612c8b1e47ab55e7")
        self.assertEqual(action_event["linked_event"], "a548ead04e53ace59cbfc271849b23d00dc9d251")
        self.assertEqual(action_event["type"], GITHUB_EVENT_ASSIGNEE)
        self.assertEqual(action_event["source"], "https://github.com/example_user/tmp")
        self.assertEqual(action_event["time"], 1768819573.0)
        self.assertEqual(action_event.data["source"], "github")
        self.assertEqual(action_event.data["username"], "example_user")
        self.assertIsNone(action_event.data["name"])
        self.assertIsNone(action_event.data["email"])
        self.assertEqual(action_event.data["uuid"], "b93094c8f58be3d61ba4d9e19a1603a18ce0e758")


if __name__ == "__main__":
    unittest.main()
