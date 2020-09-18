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

from .meta import NAME, VERSION, DESCRIPTION

parser = argparse.ArgumentParser(
    prog='{} {}'.format(NAME, VERSION),
    description=DESCRIPTION,
    epilog='The Cake is a lie.',
)

group_main = parser.add_argument_group(title='Main options')

group_main.add_argument(
    '-i', '--input',
    help='Input files to configuration profile set',
    default=[],
    action='append'
)

group_main.add_argument(
    '-o', '--output',
    help='Output path to generated files to'
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
