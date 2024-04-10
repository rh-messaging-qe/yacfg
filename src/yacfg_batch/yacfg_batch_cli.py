#! /usr/bin/env -S python3 -sP

from __future__ import print_function

import logging
import pathlib
import sys

# `from yacfg_batch import ...` may target both src/yacfg/yacfg_batch/__init__.py
# and src/yacfg/yacfg_batch/yacfg_batch.py (which is on sys.path when running
# this file directly). Remove the undesirable sys.path entry to prevent `ImportError`s.
try:
    sys.path.remove(str(pathlib.Path(__file__).resolve().parent))
except ValueError:
    pass

from yacfg import NAME, logger_settings

from yacfg_batch import __version__
from yacfg_batch.cli_arguments import parser
from yacfg_batch.yacfg_batch import generate

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
        error("Missing parameter input, cannot work without input.", 2)

    if options.input:
        generate(options.input, options.output)

    print("have a nice day.")


if __name__ == "__main__":
    main()
