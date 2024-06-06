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

import importlib
import pkgutil

from collections.abc import Iterator, Generator
from typing import Any

from cloudevents.http import CloudEvent

from .events import core


class Eventizer:
    """Abstract class to eventize Perceval data."""

    def eventize(self, raw_items: Iterator[dict[str, Any]]) -> Generator[dict[str, Any]]:
        for raw_item in raw_items:
            yield from self.eventize_item(raw_item)

    def eventize_item(self, raw_item: dict[str, Any]) -> list[CloudEvent]:
        raise NotImplementedError


def eventize(name: str, raw_items: Iterator[dict[str, Any]]) -> Generator[dict[str, Any]]:
    """Eventize data of a given type."""

    eventizers = find_eventizers(core)

    try:
        eventizer = eventizers[name]()
    except KeyError:
        raise ValueError(f"Unknown eventizer {name}")

    yield from eventizer.eventize(raw_items)


def find_eventizers(top_package: str) -> dict[str, Eventizer]:
    """Find available eventizers.

    Look for the `Eventizer` classes under `top_package`
    and its sub-packages. When `top_package` defines a namespace,
    classes under that same namespace will be found too.

    :param top_package: package storing eventizer classes

    :returns: a dict with `Eventizer`
    """
    candidates = pkgutil.walk_packages(top_package.__path__,
                                       prefix=top_package.__name__ + '.')

    modules = [name for _, name, is_pkg in candidates if not is_pkg]

    return _import_eventizers(modules)


def _import_eventizers(modules):
    for module in modules:
        importlib.import_module(module)

    klasses = _find_classes(Eventizer, modules)

    eventizers = {name: kls for name, kls in klasses}

    return eventizers


def _find_classes(parent, modules):
    parents = parent.__subclasses__()

    while parents:
        kls = parents.pop()

        m = kls.__module__

        if m not in modules:
            continue

        name = m.split('.')[-1]
        parents.extend(kls.__subclasses__())

        yield name, kls
