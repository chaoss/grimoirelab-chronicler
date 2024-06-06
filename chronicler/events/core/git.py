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

from ...eventizer import Eventizer


class GitEventizer(Eventizer):

    def eventize_item(self, raw_item: dict[str, Any]) -> list[dict[str, Any]]:
        if raw_item['backend_name'] != 'Git':
            raise ValueError("Raw item isn't a Git item.")
        if raw_item['category'] not in ['commit']:
            raise ValueError("Raw item category is invalid.")

        attributes = {
            "id": raw_item['uuid'],
            "type": "org.grimoirelab.events.git.commit",
            "source": raw_item['origin'],
            "time": raw_item['updated_on'],
        }

        event = CloudEvent(attributes, raw_item['data'])

        return [event]
