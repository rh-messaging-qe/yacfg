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
import os
import sys

from .config_data import RenderOptions
from .yacfg import generate
from .cli_arguments import parser, boolize, parse_key_value_list
from .exceptions import TemplateError, ProfileError, GenerationError
from .meta import VERSION, NAME
from .output import (
    new_profile, new_profile_rendered,
    new_template, export_tuning_variables
)
from .query import list_templates, list_profiles

from . import logger_settings

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

    # post-process direct options
    if options.opt:
        # list is because generate api expects list of tuning dicts
        try:
            # false negative, there is not type mismatch, ArgParse
            # does not parse KEY=VALUE pairs automatically
            # noinspection PyTypeChecker
            options.opt = [parse_key_value_list(options.opt)]
        except ValueError as exc:
            error(exc, 2)

    LOG.debug('Direct Tuning options %s', options.opt)

    do_not_generate = False

    if options.version:
        print(VERSION)
        return

    if options.list_templates:
        LOG.info('Available Templates:')
        print(os.linesep.join(list_templates()))
        return

    if options.list_profiles:
        LOG.info('Available Profiles:')
        print(os.linesep.join(list_profiles()))
        return

    error_do_not_generate = False

    if options.new_profile or options.new_profile_static:
        do_not_generate = True
        if not options.profile:
            error('Missing parameters profile', 0)
            error_do_not_generate = True
        else:
            try:
                if options.new_profile:
                    new_profile(options.profile, options.new_profile)
                if options.new_profile_static:
                    new_profile_rendered(
                        profile=options.profile,
                        dest_profile=options.new_profile_static,
                        tuning_files=options.tune,
                        tuning_data_list=options.opt,
                    )
            except (ProfileError, IOError, OSError) as exc:
                error(exc, 0)
                error_do_not_generate = True

    if options.export_tuning:
        do_not_generate = True
        if not options.profile:
            error('Missing parameters profile', 0)
            error_do_not_generate = True
        else:
            try:
                export_tuning_variables(options.profile, options.export_tuning)
            except (ProfileError, IOError, OSError) as exc:
                error(exc, 0)
                error_do_not_generate = True

    if options.new_template:
        do_not_generate = True
        if not options.template:
            error('Missing parameter template, cannot export', 0)
            error_do_not_generate = True
        else:
            try:
                new_template(options.template, options.new_template)
            except (TemplateError, IOError, OSError) as exc:
                error(exc, 0)
                error_do_not_generate = True

    if error_do_not_generate:
        error('Cannot continue due to existing above problems', 2)

    # Generator barrier for actions that prevents generation
    if do_not_generate:
        sys.exit(0)

    if not options.profile:
        error('Missing parameters profile', 0)
        error_do_not_generate = True

    if error_do_not_generate:
        # parser.print_help()
        error('Cannot continue due to existing above problems', 2)

    # Tune up render options
    render_options = RenderOptions(
        boolize(options.render_generator_notice),
        boolize(options.render_licenses),
    )

    try:
        generate(
            profile=options.profile,
            template=options.template,
            output_path=options.output,
            output_filter=options.filter,
            render_options=render_options,
            tuning_files_list=options.tune,
            tuning_data_list=options.opt,
            write_profile_data=options.save_effective_profile
        )
    except TemplateError as exc:
        error(exc)
    except ProfileError as exc:
        error(exc)
    except GenerationError as exc:
        error(exc, 1)


if __name__ == '__main__':
    main()
