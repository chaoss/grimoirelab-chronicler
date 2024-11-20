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
import sys

import click
import cloudevents.conversion

from ._version import __version__
from .eventizer import eventize


@click.command
@click.option(
    "--input",
    help="File with perceval items",
    type=click.File("r"),
    default=sys.stdin
)
@click.option(
    "--output",
    help="File where events will be written",
    type=click.File("w"),
    default=sys.stdout
)
@click.option(
    "--json-line",
    help="Produce a JSON line for each output item",
    is_flag=True,
    show_default=True,
    default=False
)
@click.argument('datasource')
@click.version_option(__version__, message="%(prog)s %(version)s")
def chronicler(datasource, input, output, json_line):
    """Generates GrimoireLab events from the items fetched by Perceval.

    The chronicler is a command line tool and a library that converts
    items generated by Perceval into events. The tool reads
    these events from the standard input or from a given file.

    To run it, you will have to give the type of items the chronicler
    is receiving with DATASOURCE argument (e.g. git, github, gitlab).

    Output is produced using JSON format. Use the option <json_line>
    to generate JSON object per line.
    """
    def _read_input(input):
        for line in input:
            yield json.loads(line)

    for item in eventize(datasource, _read_input(input)):
        if json_line:
            obj = json.dumps(cloudevents.conversion.to_dict(item),
                             separators=(',', ':'), sort_keys=True)
        else:
            obj = json.dumps(cloudevents.conversion.to_dict(item),
                             indent=4, sort_keys=True)
        output.write(obj)
        output.write('\n')
