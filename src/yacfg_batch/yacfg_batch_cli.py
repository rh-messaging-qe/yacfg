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

from __future__ import print_function

import logging
import sys

from yacfg import logger_settings
from yacfg.meta import NAME
from .yacfg_batch import generate
from .cli_arguments import parser
from . import __version__

logger_settings.config_console_logger()

LOG = logging.getLogger(NAME)


def error(msg, ecode=2):
    LOG.error(msg)
    if ecode != 0:
        sys.exit(ecode)


def main():
    options = parser.parse_args()

    # logging adjustments
    root_logger = logging.getLogger()
    if options.verbose:
        root_logger.setLevel(logging.INFO)
    if options.quiet:
        root_logger.setLevel(logging.ERROR)
    if options.debug:
        root_logger.setLevel(logging.DEBUG)

    if options.version:
        print(__version__)
        return

    if not options.input:
        error(
            'Missing parameter input, cannot work without input.',
            2
        )

    if options.input:
        generate(options.input, options.output)

    print('have a nice day.')


if __name__ == '__main__':
    main()
