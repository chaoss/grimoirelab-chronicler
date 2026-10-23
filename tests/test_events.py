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

import unittest

from chronicler.eventizer import GrimoireLabEvent
from chronicler.events.core import events


def all_event_classes(parent=GrimoireLabEvent):
    for kls in parent.__subclasses__():
        yield kls
        yield from all_event_classes(kls)


class EventTestCase(unittest.TestCase):
    """Unit tests for Event classes"""

    def test_to_cloudevent(self):
        """Check if attributes and data are split correctly"""

        event = events.CommitFileAdded(
            id="1234",
            linkedevent="abcd",
            source="https://example.git",
            datasource="git",
            time=1344966351.0,
            commit="c6ba8f7a",
            filename="ddd/finalthing",
            modes=["000000", "100644"],
            indexes=["0000000...", "e69de29..."],
        )

        cloudevent = event.to_cloudevent()

        self.assertEqual(cloudevent["id"], "1234")
        self.assertEqual(cloudevent["linkedevent"], "abcd")
        self.assertEqual(cloudevent["type"], "org.grimoirelab.events.commit.file.added")
        self.assertEqual(cloudevent["datasource"], "git")
        self.assertEqual(cloudevent["source"], "https://example.git")
        self.assertEqual(cloudevent["time"], 1344966351.0)

        self.assertEqual(
            cloudevent.data,
            {
                "commit": "c6ba8f7a",
                "filename": "ddd/finalthing",
                "modes": ["000000", "100644"],
                "indexes": ["0000000...", "e69de29..."],
                "similarity": None,
                "new_filename": None,
                "added_lines": None,
                "deleted_lines": None,
            },
        )

    def test_datasource_is_given_on_creation(self):
        """Check that the data source is set by whoever creates the event"""

        kwargs = {
            "id": "1234",
            "source": "https://example.git",
            "time": 1344966351.0,
            "commit": "c6ba8f7a",
            "filename": "ddd/finalthing",
            "modes": [],
            "indexes": [],
        }

        event = events.CommitFileAdded(datasource="git", **kwargs)
        self.assertEqual(event.to_cloudevent()["datasource"], "git")

        event = events.CommitFileAdded(datasource="other", **kwargs)
        self.assertEqual(event.to_cloudevent()["datasource"], "other")

        # The data source is an attribute, not part of the data
        self.assertNotIn("datasource", event.to_cloudevent().data)

    def test_datasource_is_required(self):
        """Check if it fails when the data source is not given"""

        with self.assertRaises(TypeError):
            events.CommitFileAdded(
                id="1234",
                source="https://example.git",
                time=1344966351.0,
                commit="c6ba8f7a",
                filename="ddd/finalthing",
                modes=[],
                indexes=[],
            )

    def test_linkedevent_is_optional(self):
        """Check that linkedevent is not set when it is not given"""

        event = events.CommitAuthoredBy(
            id="1234",
            source="https://example.git",
            datasource="git",
            time=1344966351.0,
            commit="c6ba8f7a",
            name="John Smith",
            username=None,
            email="jsmith@example.com",
            uuid="abcd",
        )

        cloudevent = event.to_cloudevent()

        self.assertNotIn("linkedevent", cloudevent.get_attributes())
        self.assertEqual(cloudevent.data["role"], "authored_by")
        self.assertEqual(cloudevent["datasource"], "git")
        self.assertNotIn("datasource", cloudevent.data)

    def test_commit_extra_fields(self):
        """Check if the extra fields of a commit are merged into the data"""

        event = events.Commit(
            id="1234",
            source="https://example.git",
            datasource="git",
            time=1344966351.0,
            author="John Smith <jsmith@example.com>",
            author_date="Tue Aug 14 14:45:51 2012 -0300",
            committer="John Smith <jsmith@example.com>",
            commit_date="Tue Aug 14 14:45:51 2012 -0300",
            commit="c6ba8f7a",
            files=[],
            message="Add one final file",
            parents=[],
            refs=[],
            extra={"Signed-off-by": ["Jane Rae <jrae@example.com>"]},
        )

        data = event.to_cloudevent().data

        self.assertEqual(data["Signed-off-by"], ["Jane Rae <jrae@example.com>"])
        self.assertNotIn("extra", data)

    def test_missing_field(self):
        """Check if it fails when a required field is missing"""

        with self.assertRaises(TypeError):
            events.CommitFileAdded(
                id="1234",
                source="https://example.git",
                datasource="git",
                time=1344966351.0,
            )

    def test_unknown_field(self):
        """Check if it fails when an unknown field is given"""

        with self.assertRaises(TypeError):
            events.CommitFileAdded(
                id="1234",
                source="https://example.git",
                datasource="git",
                time=1344966351.0,
                commit="c6ba8f7a",
                filename="ddd/finalthing",
                modes=[],
                indexes=[],
                unknown="value",
            )

    def test_event_definitions(self):
        """Check that concrete events define their type and describe their fields"""

        types = []

        for kls in all_event_classes():
            if "TYPE" not in vars(kls):
                continue

            self.assertTrue(kls.TYPE.startswith("org.grimoirelab.events."), kls)

            for f in kls.data_fields():
                self.assertIn("description", f.metadata, f"{kls.__name__}.{f.name}")

            types.append(kls.TYPE)

        self.assertGreater(len(types), 0)
        self.assertEqual(len(types), len(set(types)), "duplicated event types")


if __name__ == "__main__":
    unittest.main()
