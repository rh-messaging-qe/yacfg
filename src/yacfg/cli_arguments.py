# Copyright 2018 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import re
import json

from .meta import NAME, DESCRIPTION
from . import __version__

parser = argparse.ArgumentParser(
    prog='{} {}'.format(NAME, __version__),
    description=DESCRIPTION,
    epilog='The Cake is a lie.',
)

# Group Main
group_main = parser.add_argument_group(title='Main options')

group_main.add_argument(
    '-t', '--template',
    help='Configuration template set name (packaged, or user provided path)'
)

group_main.add_argument(
    '-p', '--profile',
    help='Configuration data profile name (packaged, or user provided path)',
)

group_main.add_argument(
    '-o', '--output',
    help='Output path to generated files to'
)

group_main.add_argument(
    '--tune',
    help=(
        'Fine tune profile variables by providing a YAML file'
        ' with values mapping (if selected profile support variables)'
    ),
    action='append',
)

group_main.add_argument(
    '--opt',
    metavar='KEY=VALUE',
    help=(
        'Fine tune one tuning value format KEY=VALUE, has higher'
        ' priority than tuning files.'
    ),
    action='append'
)

# Group Extra
group_extra = parser.add_argument_group(
    title='Extra Options'
)

group_extra.add_argument(
    '--extra-properties',
    help='Extra properties (key-value pairs) that can be used by specific templates'
         ' Example: "{x:y,a:b}"',
    type=json.loads
)

group_extra.add_argument(
    '-f', '--filter',
    help='Regular expression enabled output filename filter,'
         ' to generate_via_tuning_files only selected config files',
    action='append',
)

group_extra.add_argument(
    '--save-effective-profile',
    help=(
        'Write used profile data to output directory,'
        ' output has to be specified'
    ),
    action='store_true'
)

# Group Render
group_render = parser.add_argument_group(title='Render options')

group_render.add_argument(
    '--render-generator-notice',
    help='Control generator notice (header) to be put into output files'
         ' (True/False)'
)

group_render.add_argument(
    '--render-licenses',
    help='Control licenses to be put into output files (True/False)'
)

# Group Query
group_query = parser.add_argument_group(title='Query options')

group_query.add_argument(
    '--list-templates',
    help='Print a list of packaged templates',
    action='store_true'
)

group_query.add_argument(
    '--list-profiles',
    help='Print a list of packaged profiles',
    action='store_true'
)

# Group Creator
group_creator = parser.add_argument_group(
    title='Creator Options',
)

group_creator.add_argument(
    '--new-profile',
    help='Export a local copy of an existing profile for further editing'
         ' (local path), you need to use profile option to select a profile'
)

group_creator.add_argument(
    '--new-profile-static',
    help='Export a local copy of a static version of an existing profile'
         ' for further editing (local path), you need to use profile'
         ' option to select a profile'
)

group_creator.add_argument(
    '--new-template',
    help='Export a local copy of selected template for further editing'
         ' (local path), you need to use template to select a template'
)

group_creator.add_argument(
    '--export-tuning',
    help='Export a local copy of profile available variables in yaml'
         ' for easy creation of tuning file (local path)'
)

# Group Logging
group_logging = parser.add_argument_group(title='Logging options')

group_logging.add_argument(
    '-q', '--quiet',
    help='Keep output to minimum, only requested data (listing) or errors',
    action='store_true'
)

group_logging.add_argument(
    '-v', '--verbose',
    help='Print generation status and user relevant info',
    action='store_true'
)

group_logging.add_argument(
    '-d', '--debug',
    help='Print debugging details',
    action='store_true'
)

# Group Misc
group_misc = parser.add_argument_group(title='Miscellaneous')

group_misc.add_argument(
    '--version',
    help='Display version information',
    action='store_true'
)

REX_BOOL_TRUE = re.compile(r'^(([Tt][Rr][Uu][Ee])|[Yy][Ee][Ss]|(1))$')
REX_BOOL_FALSE = re.compile(r'^(([Ff][Aa][Ll][Ss][Ee])|([Nn][Oo])|(0))$')


def boolize(data):
    """Conver input values from string to bool if possible

    :param data: input data from argparse
    :type data: str
    :return: converted boolean value, or None if not specified
    :rtype: bool or None

    :raises ValueError: if conversion failed
    """
    if data is None:
        return None
    if REX_BOOL_TRUE.match(data):
        return True
    if REX_BOOL_FALSE.match(data):
        return False
    raise ValueError('Cannot convert input option "%s" to bool' % data)


def split_key_value(item):
    """Split KEY=VALUE specifier or raise an ValueError exception.

    :param item: input KEY=VALUE string option.
    :type item: str

    :raises ValueError: if cannot split

    :return: pair of split key and value
    :rtype: str, str
    """
    try:
        key, value = item.split('=', 1)
    except ValueError:
        raise ValueError('Missing KEY=VALUE pair in option "{}"'.format(item))
    return key, value


def parse_key_value_list(items):
    """Split all KEY=VALUE items in a list of such options.

    :param items: list of KEY=VALUE string options to be split.
    :type items: list[str]

    :raises ValueError: if any option cannot be split.

    :return: a map of KEY: VALUE split options
    :rtype: dict
    """
    result = dict([split_key_value(item) for item in items])
    return result
