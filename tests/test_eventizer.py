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

import os
import unittest

from typing import Any

from cloudevents.http import CloudEvent

from chronicler.eventizer import (Eventizer,
                                  eventize)


class EventizerTestingClass(Eventizer):
    """Subclass of Eventizer for testing"""

    def eventize_item(self, raw_item: dict[str, Any]) -> list[CloudEvent]:
        attributes = {
            "id": raw_item['id'],
            "type": "test_event",
            "source": "test",
            "time": raw_item['time'],
        }
        return [CloudEvent(attributes, raw_item['data'])]


class TestEventizer(unittest.TestCase):
    """Unit tests for Eventizer class"""

    def test_eventize_single_item(self):
        """Check if a single item is eventized"""

        eventizer = EventizerTestingClass()

        raw_items = iter([
            {'id': 1, 'time': '2024-06-24T12:00:00Z', 'data': 'item1 data'}
        ])
        events = list(eventizer.eventize(raw_items))

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['id'], 1)
        self.assertEqual(events[0]['type'], 'test_event')
        self.assertEqual(events[0]['source'], 'test')
        self.assertEqual(events[0]['time'], '2024-06-24T12:00:00Z')
        self.assertEqual(events[0].data, 'item1 data')

    def test_eventize_multiple_items(self):
        """Check if multiple items are eventized"""

        eventizer = EventizerTestingClass()

        raw_items = iter([
            {'id': 1, 'time': '2024-06-24T12:00:00Z', 'data': 'item1 data'},
            {'id': 2, 'time': '2024-06-24T13:00:00Z', 'data': 'item2 data'}
        ])
        events = list(eventizer.eventize(raw_items))

        self.assertEqual(len(events), 2)

        self.assertEqual(events[0]['id'], 1)
        self.assertEqual(events[0]['type'], 'test_event')
        self.assertEqual(events[0]['source'], 'test')
        self.assertEqual(events[0]['time'], '2024-06-24T12:00:00Z')
        self.assertEqual(events[0].data, 'item1 data')

        self.assertEqual(events[1]['id'], 2)
        self.assertEqual(events[1]['type'], 'test_event')
        self.assertEqual(events[1]['source'], 'test')
        self.assertEqual(events[1]['time'], '2024-06-24T13:00:00Z')
        self.assertEqual(events[1].data, 'item2 data')

    def test_eventize_empty(self):
        """Check there's no failure for empty list of items"""

        eventizer = EventizerTestingClass()

        raw_items = iter([])
        events = list(eventizer.eventize(raw_items))

        self.assertEqual(len(events), 0)


class TestEventize(unittest.TestCase):
    """Unit tests for eventize function"""

    def setUp(self) -> None:
        os.environ['CHRONICLER_EVENTIZERS'] = 'tests.events_test_pck'

    def tearDown(self) -> None:
        os.environ['CHRONICLER_EVENTIZERS'] = 'chronicler.events'

    def test_eventize_items(self):
        """Check if items are eventized"""

        raw_items = iter([
            {'id': 1, 'time': '2024-06-24T12:00:00Z', 'data': 'item1 data'},
            {'id': 2, 'time': '2024-06-24T13:00:00Z', 'data': 'item2 data'}
        ])
        events = list(eventize('eventizer_test', raw_items))

        self.assertEqual(len(events), 2)

        self.assertEqual(events[0]['id'], 1)
        self.assertEqual(events[0]['type'], 'test_event')
        self.assertEqual(events[0]['source'], 'test')
        self.assertEqual(events[0]['time'], '2024-06-24T12:00:00Z')
        self.assertEqual(events[0].data, 'item1 data')

        self.assertEqual(events[1]['id'], 2)
        self.assertEqual(events[1]['type'], 'test_event')
        self.assertEqual(events[1]['source'], 'test')
        self.assertEqual(events[1]['time'], '2024-06-24T13:00:00Z')
        self.assertEqual(events[1].data, 'item2 data')

    def test_eventizer_not_found(self):
        """Check if an exception is raised when an eventizer is not found"""

        raw_items = iter([
            {'id': 1, 'time': '2024-06-24T12:00:00Z', 'data': 'item1 data'},
            {'id': 2, 'time': '2024-06-24T13:00:00Z', 'data': 'item2 data'}
        ])

        with self.assertRaisesRegex(ValueError, 'fake_eventizer'):
            _ = list(eventize('fake_eventizer', raw_items))


if __name__ == '__main__':
    unittest.main()
