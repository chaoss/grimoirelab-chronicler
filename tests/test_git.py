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

from chronicler.events.core.git import (GitEventizer,
                                        GIT_EVENT_COMMIT,
                                        GIT_EVENT_MERGE_COMMIT,
                                        GIT_EVENT_ACTION_ADDED,
                                        GIT_EVENT_ACTION_MODIFIED,
                                        GIT_EVENT_ACTION_REPLACED)


class GitEventizerTestCase(unittest.TestCase):
    """Unit tests for GitEventizer class"""

    def test_eventize_item_commit(self):
        """Check if it produces the right events from a commit"""

        eventizer = GitEventizer()

        raw_item = {
            "backend_name": "Git",
            "backend_version": "1.0.0",
            "category": "commit",
            "classified_fields_filtered": None,
            "data": {
                "Author": "Eduardo Morais <companheiro.vermelho@example.com>",
                "AuthorDate": "Tue Aug 14 14:45:51 2012 -0300",
                "Commit": "Eduardo Morais <companheiro.vermelho@example.com>",
                "CommitDate": "Tue Aug 14 14:45:51 2012 -0300",
                "commit": "c6ba8f7a1058db3e6b4bc6f1090e932b107605fb",
                "files": [
                    {
                        "action": "A",
                        "added": "0",
                        "file": "ddd/finalthing",
                        "indexes": [
                            "0000000...",
                            "e69de29..."
                        ],
                        "modes": [
                            "000000",
                            "100644"
                        ],
                        "removed": "0"
                    }
                ],
                "message": "Add one final file",
                "parents": [
                    "c0d66f92a95e31c77be08dc9d0f11a16715d1885"
                ],
                "refs": []
            },
            "offset": "c6ba8f7a1058db3e6b4bc6f1090e932b107605fb",
            "origin": "https://example.git",
            "perceval_version": "1.0.0",
            "search_fields": {
                "item_id": "c6ba8f7a1058db3e6b4bc6f1090e932b107605fb"
            },
            "tag": "https://example.git",
            "timestamp": 1719313540.7217,
            "updated_on": 1344966351.0,
            "uuid": "439b7a02af9b8f6041951b3b2dc96b6929ea94a8"
        }

        events = eventizer.eventize_item(raw_item)

        self.assertEqual(len(events), 2)

        commit_event = events[0]
        self.assertEqual(commit_event['id'], '439b7a02af9b8f6041951b3b2dc96b6929ea94a8')
        self.assertEqual(commit_event['type'], GIT_EVENT_COMMIT)
        self.assertEqual(commit_event['source'], 'https://example.git')
        self.assertEqual(commit_event['time'], 1344966351.0)
        self.assertEqual(commit_event.data['message'], "Add one final file")

        action_event = events[1]
        self.assertEqual(action_event['id'], '6b93bbfcd583d9712179eee4801750023f17364a')
        self.assertEqual(action_event['type'], GIT_EVENT_ACTION_ADDED)
        self.assertEqual(action_event['source'], 'https://example.git')
        self.assertEqual(action_event['time'], 1344966351.0)
        self.assertEqual(action_event.data['filename'], 'ddd/finalthing')
        self.assertEqual(action_event.data['added_lines'], '0')
        self.assertEqual(action_event.data['deleted_lines'], '0')

    def test_eventize_item_merge_commit(self):
        """Check if it produces the right events from a merge commit"""

        eventizer = GitEventizer()

        raw_item = {
            "backend_name": "Git",
            "backend_version": "1.0.0",
            "category": "commit",
            "classified_fields_filtered": None,
            "data": {
                "Author": "Zhongpeng Lin (\u6797\u4e2d\u9e4f) <lin.zhp@example.com>",
                "AuthorDate": "Tue Feb 11 22:10:39 2014 -0800",
                "Commit": "Zhongpeng Lin (\u6797\u4e2d\u9e4f) <lin.zhp@example.com>",
                "CommitDate": "Tue Feb 11 22:10:39 2014 -0800",
                "Merge": "ce8e0b8 51a3b65",
                "commit": "456a68ee1407a77f3e804a30dff245bb6c6b872f",
                "files": [
                    {
                        "action": "MR",
                        "added": "1",
                        "file": "aaa/otherthing.renamed",
                        "indexes": [
                            "e69de29...",
                            "58a6c75...",
                            "58a6c75..."
                        ],
                        "modes": [
                            "100644",
                            "100644",
                            "100644"
                        ],
                        "removed": "0"
                    }
                ],
                "message": "Merge branch 'lzp'\n\nConflicts:\n\taaa/otherthing",
                "parents": [
                    "ce8e0b86a1e9877f42fe9453ede418519115f367",
                    "51a3b654f252210572297f47597b31527c475fb8"
                ],
                "refs": [
                    "HEAD -> refs/heads/master"
                ]
            },
            "offset": "456a68ee1407a77f3e804a30dff245bb6c6b872f",
            "origin": "https://example.git",
            "perceval_version": "1.0.1",
            "search_fields": {
                "item_id": "456a68ee1407a77f3e804a30dff245bb6c6b872f"
            },
            "tag": "https://example.git",
            "timestamp": 1719313540.7196,
            "updated_on": 1392185439.0,
            "uuid": "2abc82e1fb2917e2fb2d7018dba6fb4b4a8c29f0"
        }

        events = eventizer.eventize_item(raw_item)

        self.assertEqual(len(events), 3)

        commit_event = events[0]
        self.assertEqual(commit_event['id'], '2abc82e1fb2917e2fb2d7018dba6fb4b4a8c29f0')
        self.assertEqual(commit_event['type'], GIT_EVENT_MERGE_COMMIT)
        self.assertEqual(commit_event['source'], 'https://example.git')
        self.assertEqual(commit_event['time'], 1392185439.0)
        self.assertEqual(commit_event.data['parents'], ["ce8e0b86a1e9877f42fe9453ede418519115f367",
                                                        "51a3b654f252210572297f47597b31527c475fb8"])

        action_event = events[1]
        self.assertEqual(action_event['id'], '1cfb8955e9bdab98dc4cf120985839683a01a310')
        self.assertEqual(action_event['type'], GIT_EVENT_ACTION_MODIFIED)
        self.assertEqual(action_event['source'], 'https://example.git')
        self.assertEqual(action_event['time'], 1392185439.0)
        self.assertEqual(action_event.data['filename'], 'aaa/otherthing.renamed')
        self.assertEqual(action_event.data['added_lines'], '1')
        self.assertEqual(action_event.data['deleted_lines'], '0')

        action_event = events[2]
        self.assertEqual(action_event['id'], 'db19cf3878cc70db807cf92e10461b60c872f73b')
        self.assertEqual(action_event['type'], GIT_EVENT_ACTION_REPLACED)
        self.assertEqual(action_event['source'], 'https://example.git')
        self.assertEqual(action_event['time'], 1392185439.0)
        self.assertEqual(action_event.data['filename'], 'aaa/otherthing.renamed')
        self.assertEqual(action_event.data['added_lines'], '1')
        self.assertEqual(action_event.data['deleted_lines'], '0')

    def test_eventize(self):
        """Check if eventizies a full set of items"""

        eventizer = GitEventizer()

        with open('data/git_commits.txt', 'r') as file:
            commits = [json.loads(line.strip()) for line in file.readlines()]

        events = list(eventizer.eventize(commits))
        self.assertEqual(len(events), 25)

    def test_eventize_item_invalid_backend(self):
        """Check invalid backend item type"""

        eventizer = GitEventizer()

        raw_item = {
            'uuid': '1234',
            'backend_name': 'GitHub',
            'category': 'commit',
            'origin': 'repo1',
            'updated_on': 1392185439.0,
            'data': {
                'files': []
            }
        }
        with self.assertRaises(ValueError) as context:
            _ = eventizer.eventize_item(raw_item)
        self.assertEqual(str(context.exception), "Item 1234 is not a 'git' item.")

    def test_eventize_item_invalid_category(self):
        """Check invalid backend item category"""

        eventizer = GitEventizer()

        raw_item = {
            'uuid': '1234',
            'backend_name': 'Git',
            'category': 'pull_request',
            'origin': 'repo1',
            'updated_on': 1392185439.0,
            'data': {
                'files': []
            }
        }
        with self.assertRaises(ValueError) as context:
            _ = eventizer.eventize_item(raw_item)
        self.assertEqual(str(context.exception), "Invalid category 'pull_request' for '1234' item.")

    def test_eventize_item_no_uuid(self):
        """Check invalid backend item category"""

        eventizer = GitEventizer()

        raw_item = {
            'backend_name': 'Git',
            'category': 'commit',
            'origin': 'repo1',
            'updated_on': 1392185439.0,
            'data': {
                'files': []
            }
        }
        with self.assertRaises(ValueError) as context:
            _ = eventizer.eventize_item(raw_item)
        self.assertEqual(str(context.exception), "'uuid' attribute not found on item.")


if __name__ == '__main__':
    unittest.main()
