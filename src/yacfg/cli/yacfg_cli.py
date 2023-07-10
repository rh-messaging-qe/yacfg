import logging
import os
import sys

from .. import NAME, __version__, logger_settings
from yacfg.cli.cli_arguments import boolize, parse_key_value_list, parser
from ..config_data import RenderOptions
from ..exceptions import GenerationError, ProfileError, TemplateError
from ..output import (
    export_tuning_variables,
    new_profile,
    new_profile_rendered,
    new_template,
)
from ..query import list_profiles, list_templates
from ..yacfg import generate

logger_settings.config_console_logger()

LOG: logging.Logger = logging.getLogger(NAME)


class CommandLineApp:
    def __init__(self):
        self.parser = parser

    def run(self, args=None):
        if args is None:
            args = sys.argv[1:]

        if len(args) == 0:
            self.parser.print_help()
            sys.exit(0)

        options = self.parser.parse_args(args)

        if len(sys.argv) == 1:
            options.print_help()
            sys.exit(0)

        # Logging adjustments
        root_logger: logging.Logger = logging.getLogger()

        if options.verbose:
            root_logger.setLevel(logging.INFO)
        if options.quiet:
            root_logger.setLevel(logging.ERROR)
        if options.debug:
            root_logger.setLevel(logging.DEBUG)

        # Post-process direct options
        if options.opt:
            LOG.debug(f"Direct Tuning options {options.opt}")
            try:
                parsed_opt = parse_key_value_list(options.opt)
                options.opt = [parsed_opt]
            except ValueError as exc:
                self.error(f"Failed to parse 'opt' argument: {exc}", 2)

        if options.version:
            print(__version__)
            return

        if options.list_templates:
            LOG.info("Available Templates:")
            print(os.linesep.join(list_templates()))
            return

        if options.list_profiles:
            LOG.info("Available Profiles:")
            print(os.linesep.join(list_profiles()))
            return

        if options.new_profile or options.new_profile_static:
            if not options.profile:
                self.error("Missing parameters profile", 0)
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
                    self.error(str(exc), 0)

        if options.export_tuning:
            if not options.profile:
                self.error("Missing parameters profile", 0)
            else:
                try:
                    export_tuning_variables(options.profile, options.export_tuning)
                except (ProfileError, IOError, OSError) as exc:
                    self.error(str(exc), 0)

        if options.new_template:
            if not options.template:
                self.error("Missing parameter template, cannot export", 0)
            else:
                try:
                    new_template(options.template, options.new_template)
                except (TemplateError, IOError, OSError) as exc:
                    self.error(str(exc), 0)

        if (
            options.new_profile
            or options.new_profile_static
            or options.export_tuning
            or options.new_template
        ):
            sys.exit(0)

        if not options.profile:
            self.error("Missing parameters profile", 0)

        render_options = RenderOptions(
            boolize(options.render_generator_notice),
            boolize(options.render_licenses),
        )

        if options.profile and options.template:
            try:
                generate(
                    profile=options.profile,
                    template=options.template,
                    output_path=options.output,
                    output_filter=options.filter,
                    render_options=render_options,
                    tuning_files_list=options.tune,
                    tuning_data_list=options.opt,
                    write_profile_data=options.save_effective_profile,
                    extra_properties_data=options.extra_properties,
                )
            except (TemplateError, ProfileError, GenerationError) as exc:
                self.error(str(exc))

    @staticmethod
    def error(msg: str, ecode: int = 2) -> None:
        LOG.error(msg)
        if ecode != 0:
            sys.exit(ecode)


def main():
    app = CommandLineApp()
    app.run()


if __name__ == "__main__":
    main()
