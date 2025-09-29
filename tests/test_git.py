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
                                        GIT_EVENT_ACTION_REPLACED,
                                        GIT_EVENT_ACTION_COPIED,
                                        GIT_EVENT_COMMIT_AUTHORED_BY,
                                        GIT_EVENT_COMMIT_COMMITTED_BY,
                                        GIT_EVENT_COMMIT_SIGNED_OFF_BY,
                                        GIT_EVENT_COMMIT_CO_AUTHORED_BY)


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

        self.assertEqual(len(events), 4)

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

        identity_event = events[2]
        self.assertEqual(identity_event['id'], 'a2adafb6271350527cf126c8ebd2ddecfccf8613')
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_AUTHORED_BY)
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1344966351.0)
        self.assertEqual(identity_event.data['name'], 'Eduardo Morais')
        self.assertEqual(identity_event.data['email'], 'companheiro.vermelho@example.com')
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], '2769070fa473431f31d871928e6d0ddb08c59f22')
        self.assertEqual(identity_event.data['role'], 'authored_by')
        self.assertEqual(identity_event.data['source'], 'git')

        identity_event = events[3]
        self.assertEqual(identity_event['id'], '0fc398a278a3a2dc11fafc9dc8274e05d1bf535a')
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_COMMITTED_BY)
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1344966351.0)
        self.assertEqual(identity_event.data['name'], 'Eduardo Morais')
        self.assertEqual(identity_event.data['email'], 'companheiro.vermelho@example.com')
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], '2769070fa473431f31d871928e6d0ddb08c59f22')
        self.assertEqual(identity_event.data['role'], 'committed_by')
        self.assertEqual(identity_event.data['source'], 'git')

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

        self.assertEqual(len(events), 5)

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

        identity_event = events[3]
        self.assertEqual(identity_event['id'], 'b59a52f21d07a33eacb2a9b202968743755f7aa6')
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_AUTHORED_BY)
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1392185439.0)
        self.assertEqual(identity_event.data['name'], 'Zhongpeng Lin (\u6797\u4e2d\u9e4f)')
        self.assertEqual(identity_event.data['email'], 'lin.zhp@example.com')
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], '5765f675858a5f6c2500337ed5af90ac648ef9e9')
        self.assertEqual(identity_event.data['role'], 'authored_by')
        self.assertEqual(identity_event.data['source'], 'git')

        identity_event = events[4]
        self.assertEqual(identity_event['id'], '281802ecda04960e5841532e78bef91652c11583')
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_COMMITTED_BY)
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1392185439.0)
        self.assertEqual(identity_event.data['name'], 'Zhongpeng Lin (\u6797\u4e2d\u9e4f)')
        self.assertEqual(identity_event.data['email'], 'lin.zhp@example.com')
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], '5765f675858a5f6c2500337ed5af90ac648ef9e9')
        self.assertEqual(identity_event.data['role'], 'committed_by')
        self.assertEqual(identity_event.data['source'], 'git')

    def test_eventize(self):
        """Check if eventizies a full set of items"""

        eventizer = GitEventizer()

        with open('data/git_commits.txt', 'r') as file:
            commits = [json.loads(line.strip()) for line in file.readlines()]

        events = list(eventizer.eventize(commits))
        self.assertEqual(len(events), 45)

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

    def test_eventize_commit_copy_files(self):
        """Check if events with multiple copied files are generated correctly with different ids"""

        eventizer = GitEventizer()

        raw_item = {
            "backend_name": "Git",
            "backend_version": "1.0.1",
            "category": "commit",
            "classified_fields_filtered": None,
            "data": {
                "Author": "Tom <tom@example.com>",
                "AuthorDate": "Mon Apr 29 16:25:56 2019 -0700",
                "Commit": "GitHub <noreply@github.com>",
                "CommitDate": "Mon Apr 29 16:25:56 2019 -0700",
                "commit": "7882c41g607ee5273da9637da0bb20ca7634cb83",
                "files": [
                    {
                        "action": "C100",
                        "added": "0",
                        "file": "packages/react-events/FocusScope.js",
                        "indexes": [
                            "2ff785ef79",
                            "2ff785ef79"
                        ],
                        "modes": [
                            "100644",
                            "100644"
                        ],
                        "newfile": "packages/react-events/drag.js",
                        "removed": "0"
                    },
                    {
                        "action": "C100",
                        "added": "0",
                        "file": "packages/react-events/FocusScope.js",
                        "indexes": [
                            "2ff785ef79",
                            "2ff785ef79"
                        ],
                        "modes": [
                            "100644",
                            "100644"
                        ],
                        "newfile": "packages/react-events/focus-scope.js",
                        "removed": "0"
                    }
                ],
                "message": "Sample message for commit",
                "parents": [
                    "43c4e5f348eb5704464886e2dc3221e347041b82"
                ],
                "refs": []
            },
            "offset": "7882c41g607ee5273da9637da0bb20ca7634cb83",
            "origin": "https://example.git",
            "perceval_version": "1.2.2",
            "search_fields": {
                "item_id": "7882c41g607ee5273da9637da0bb20ca7634cb83"
            },
            "tag": "https://example.git",
            "timestamp": 1.748521396234826E9,
            "updated_on": 1.556580356E9,
            "uuid": "6b4393b86512afc2e6757a6781e6018a661a72b0"
        }

        events = eventizer.eventize_item(raw_item)

        self.assertEqual(len(events), 5)

        commit_event = events[0]
        self.assertEqual(commit_event['id'], '6b4393b86512afc2e6757a6781e6018a661a72b0')
        self.assertEqual(commit_event['type'], GIT_EVENT_COMMIT)
        self.assertEqual(commit_event['source'], 'https://example.git')
        self.assertEqual(commit_event['time'], 1556580356.0)
        self.assertEqual(commit_event.data['message'], "Sample message for commit")

        action_event = events[1]
        self.assertEqual(action_event['id'], 'b911ec8df7e804b40dddb5f402e82ae816283e9c')
        self.assertEqual(action_event['linked_event'], '6b4393b86512afc2e6757a6781e6018a661a72b0')
        self.assertEqual(action_event['type'], GIT_EVENT_ACTION_COPIED)
        self.assertEqual(action_event['source'], 'https://example.git')
        self.assertEqual(action_event['time'], 1556580356.0)
        self.assertEqual(action_event.data['filename'], 'packages/react-events/FocusScope.js')
        self.assertEqual(action_event.data['new_filename'], 'packages/react-events/drag.js')
        self.assertEqual(action_event.data['added_lines'], '0')
        self.assertEqual(action_event.data['deleted_lines'], '0')

        action_event = events[2]
        self.assertEqual(action_event['id'], '5e1d30f0fd85e34cb08987bbb202201a31769b39')
        self.assertEqual(action_event['linked_event'], '6b4393b86512afc2e6757a6781e6018a661a72b0')
        self.assertEqual(action_event['type'], GIT_EVENT_ACTION_COPIED)
        self.assertEqual(action_event['source'], 'https://example.git')
        self.assertEqual(action_event['time'], 1556580356.0)
        self.assertEqual(action_event.data['filename'], 'packages/react-events/FocusScope.js')
        self.assertEqual(action_event.data['new_filename'], 'packages/react-events/focus-scope.js')
        self.assertEqual(action_event.data['added_lines'], '0')
        self.assertEqual(action_event.data['deleted_lines'], '0')

        identity_event = events[3]
        self.assertEqual(identity_event['id'], '8bae13d82339fd466ff8e2ed70af415f15a579a1')
        self.assertEqual(identity_event['linked_event'], '6b4393b86512afc2e6757a6781e6018a661a72b0')
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_AUTHORED_BY)
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1556580356.0)
        self.assertEqual(identity_event.data['name'], 'Tom')
        self.assertEqual(identity_event.data['email'], 'tom@example.com')
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], '1e575ef3e76f834094db7a3d1f2975c2de1a76e8')
        self.assertEqual(identity_event.data['role'], 'authored_by')
        self.assertEqual(identity_event.data['source'], 'git')

        identity_event = events[4]
        self.assertEqual(identity_event['id'], '8130e148d53d37198ebc63c95bf9c2691b75dab6')
        self.assertEqual(identity_event['linked_event'], '6b4393b86512afc2e6757a6781e6018a661a72b0')
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_COMMITTED_BY)
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1556580356.0)
        self.assertEqual(identity_event.data['name'], 'GitHub')
        self.assertEqual(identity_event.data['email'], 'noreply@github.com')
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], 'c780b9e5b86174118a9dbc1b738e9cd0e5fa3566')
        self.assertEqual(identity_event.data['role'], 'committed_by')
        self.assertEqual(identity_event.data['source'], 'git')

    def test_eventize_identities_trailers(self):
        """Check if identities are correctly extracted from Signed-off-by and other trailers"""

        eventizer = GitEventizer()

        raw_item = {
            "backend_name": "Git",
            "backend_version": "1.0.0",
            "category": "commit",
            "classified_fields_filtered": None,
            "data": {
                "Author": "Tom <tom@example.com>",
                "AuthorDate": "Tue Aug 14 14:45:51 2012 -0300",
                "Commit": "Tom <tom@example.com>",
                "CommitDate": "Tue Aug 14 14:45:51 2012 -0300",
                "commit": "c6ba8f7a1058db3e6b4bc6f1090e932b107605fb",
                "Signed-off-by": ["Tom Signature <tom_signature@example.com>"],
                "Co-authored-by": ["User name 2 <user2@example.com>"],
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
                "message": "Add one final file\n\n"
                           "Signed-off-by: Tom Signature <tom_signature@example.com>\n"
                           "Co-authored-by: User name 2 <user2@example.com>\n",
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

        self.assertEqual(len(events), 6)

        self.assertEqual(events[0]['type'], GIT_EVENT_COMMIT)

        self.assertEqual(events[1]['type'], GIT_EVENT_ACTION_ADDED)

        self.assertEqual(events[2]['type'], GIT_EVENT_COMMIT_AUTHORED_BY)
        self.assertEqual(events[2]['id'], '2ca3091ec32044d2f7db03314187c01f6aa01570')
        self.assertEqual(events[2].data['name'], 'Tom')
        self.assertEqual(events[2].data['email'], 'tom@example.com')
        self.assertIsNone(events[2].data['username'])
        self.assertEqual(events[2].data['uuid'], '1e575ef3e76f834094db7a3d1f2975c2de1a76e8')
        self.assertEqual(events[2].data['role'], 'authored_by')

        self.assertEqual(events[3]['type'], GIT_EVENT_COMMIT_COMMITTED_BY)
        self.assertEqual(events[3]['id'], '5de756d0fa9844dfc5c3f0f31a4920506a729e09')
        self.assertEqual(events[3].data['name'], 'Tom')
        self.assertEqual(events[3].data['email'], 'tom@example.com')
        self.assertIsNone(events[3].data['username'])
        self.assertEqual(events[3].data['uuid'], '1e575ef3e76f834094db7a3d1f2975c2de1a76e8')
        self.assertEqual(events[3].data['role'], 'committed_by')

        self.assertEqual(events[4]['type'], GIT_EVENT_COMMIT_CO_AUTHORED_BY)
        self.assertEqual(events[4]['id'], '54cbd7350d51931f531eafa0499f144147017273')
        self.assertEqual(events[4].data['name'], 'User name 2')
        self.assertEqual(events[4].data['email'], 'user2@example.com')
        self.assertIsNone(events[4].data['username'])
        self.assertEqual(events[4].data['uuid'], 'a440312a4ceb222ac7ea41f87e21e71625fe04b1')
        self.assertEqual(events[4].data['role'], 'co_authored_by')

        self.assertEqual(events[5]['type'], GIT_EVENT_COMMIT_SIGNED_OFF_BY)
        self.assertEqual(events[5]['id'], '893f18a7deef6eecbc25db5f576f6840c8fde71e')
        self.assertEqual(events[5].data['name'], 'Tom Signature')
        self.assertEqual(events[5].data['email'], 'tom_signature@example.com')
        self.assertIsNone(events[5].data['username'])
        self.assertEqual(events[5].data['uuid'], '471cc541d28b7e8af552605db75e3b17b79e34fa')
        self.assertEqual(events[5].data['role'], 'signed_off_by')

    def test_eventize_item_pair_programming(self):
        """Check if identities are correctly extracted from Pair programming authors and commiters"""

        eventizer = GitEventizer()

        raw_item = {
            "backend_name": "Git",
            "backend_version": "1.0.0",
            "category": "commit",
            "classified_fields_filtered": None,
            "data": {
                "Author": "José Pérez, Sherlock Holmes & John Smith <foo@example.com>",
                "AuthorDate": "Tue Aug 14 14:45:51 2012 -0300",
                "Commit": "José Pérez and Sherlock Holmes <foo@example.com>",
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
                "message": "Add one final file\n\n"
                           "Signed-off-by: Tom Signature <tom_signature@example.com>\n"
                           "Co-authored-by: User name 2 <user2@example.com>\n",
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
        self.assertEqual(len(events), 9)

        self.assertEqual(events[0]['type'], GIT_EVENT_COMMIT)

        self.assertEqual(events[1]['type'], GIT_EVENT_ACTION_ADDED)

        identity_event = events[2]
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_AUTHORED_BY)
        self.assertEqual(identity_event['id'], 'd79b2902045c0caa80a862f1b265cf8b9b949062')
        self.assertEqual(identity_event['linked_event'], '439b7a02af9b8f6041951b3b2dc96b6929ea94a8')
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event.data['name'], 'José Pérez')
        self.assertIsNone(identity_event.data['email'])
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], '8b5489a079c86da145d023d251f0b005f26ac81c')
        self.assertEqual(identity_event.data['role'], 'authored_by')
        self.assertEqual(identity_event.data['source'], 'git')

        identity_event = events[3]
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_AUTHORED_BY)
        self.assertEqual(identity_event['id'], 'e9be85bc27c70ab87ca1f598af9e38c6f67e5f22')
        self.assertEqual(identity_event['linked_event'], '439b7a02af9b8f6041951b3b2dc96b6929ea94a8')
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event.data['source'], 'git')
        self.assertEqual(identity_event.data['name'], 'Sherlock Holmes')
        self.assertIsNone(identity_event.data['email'])
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], 'adf5581882b665c682e028aaf53d9bde152d0d2c')
        self.assertEqual(identity_event.data['role'], 'authored_by')

        identity_event = events[4]
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_AUTHORED_BY)
        self.assertEqual(identity_event['id'], '26266220f5b0b1d071875fcdad8d1896058829b6')
        self.assertEqual(identity_event['linked_event'], '439b7a02af9b8f6041951b3b2dc96b6929ea94a8')
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1344966351.0)
        self.assertEqual(identity_event.data['source'], 'git')
        self.assertEqual(identity_event.data['name'], 'John Smith')
        self.assertIsNone(identity_event.data['email'])
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], '8cadc67173d8293b8f9ddeb38bffe7900531d26d')
        self.assertEqual(identity_event.data['role'], 'authored_by')

        identity_event = events[5]
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_AUTHORED_BY)
        self.assertEqual(identity_event['id'], '8579f6957759f5e991283eb9d2912059c8f92b0f')
        self.assertEqual(identity_event['linked_event'], '439b7a02af9b8f6041951b3b2dc96b6929ea94a8')
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1344966351.0)
        self.assertEqual(identity_event.data['source'], 'git')
        self.assertIsNone(identity_event.data['name'])
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['email'], 'foo@example.com')
        self.assertEqual(identity_event.data['uuid'], '6e20e8da92218fb76ad5d8d8e4ffd05cbae28ff7')
        self.assertEqual(identity_event.data['role'], 'authored_by')

        identity_event = events[6]
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_COMMITTED_BY)
        self.assertEqual(identity_event['id'], '529c08c3a8ce575f19b3f4ac87c162570122307c')
        self.assertEqual(identity_event['linked_event'], '439b7a02af9b8f6041951b3b2dc96b6929ea94a8')
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1344966351.0)
        self.assertEqual(identity_event.data['source'], 'git')
        self.assertEqual(identity_event.data['name'], 'José Pérez')
        self.assertIsNone(identity_event.data['email'])
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], '8b5489a079c86da145d023d251f0b005f26ac81c')
        self.assertEqual(identity_event.data['role'], 'committed_by')

        identity_event = events[7]
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_COMMITTED_BY)
        self.assertEqual(identity_event['id'], '829358b31ca25a0d9caddd5c343f8cd83b7859f4')
        self.assertEqual(identity_event['linked_event'], '439b7a02af9b8f6041951b3b2dc96b6929ea94a8')
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1344966351.0)
        self.assertEqual(identity_event.data['source'], 'git')
        self.assertEqual(identity_event.data['name'], 'Sherlock Holmes')
        self.assertIsNone(identity_event.data['email'])
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['uuid'], 'adf5581882b665c682e028aaf53d9bde152d0d2c')
        self.assertEqual(identity_event.data['role'], 'committed_by')

        identity_event = events[8]
        self.assertEqual(identity_event['type'], GIT_EVENT_COMMIT_COMMITTED_BY)
        self.assertEqual(identity_event['id'], 'd5413231296d17b5ef0a68710465e97c99993156')
        self.assertEqual(identity_event['linked_event'], '439b7a02af9b8f6041951b3b2dc96b6929ea94a8')
        self.assertEqual(identity_event['source'], 'https://example.git')
        self.assertEqual(identity_event['time'], 1344966351.0)
        self.assertEqual(identity_event.data['source'], 'git')
        self.assertIsNone(identity_event.data['name'])
        self.assertIsNone(identity_event.data['username'])
        self.assertEqual(identity_event.data['email'], 'foo@example.com')
        self.assertEqual(identity_event.data['uuid'], '6e20e8da92218fb76ad5d8d8e4ffd05cbae28ff7')
        self.assertEqual(identity_event.data['role'], 'committed_by')


if __name__ == '__main__':
    unittest.main()
