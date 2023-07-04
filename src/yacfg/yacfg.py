import logging
import os
from typing import Any, Dict, List, Optional

import yaml
from jinja2 import Environment, Template

from . import NAME
from .config_data import RenderOptions, add_render_config, add_template_metadata
from .exceptions import GenerationError, TemplateError
from .files import ensure_output_path, get_output_filename
from .output import write_output
from .profiles import get_tuned_profile
from .query import filter_template_list, get_main_template_list
from .templates import get_template_environment

# workaround for flake8: F401 'jinja2.Template' imported but unused
_t = Template
_e = Environment

LOG: logging.Logger = logging.getLogger(NAME)


def generate_core(
    config_data: Dict[str, Any],
    tuned_profile: Optional[str] = None,
    template: Optional[str] = None,
    output_path: Optional[str] = None,
    output_filter: Optional[List[str]] = None,
    render_options: Optional[RenderOptions] = None,
    write_profile_data: bool = False,
    extra_properties_data: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Core of the generator, gets complete dataset with selected
    template in config data or explicitly selected via template
    parameter at minimum, and generates outputs. If requested, it writes
    to file.

    :param config_data: complete and tuned config data
        or path to user provided profile
    :type config_data: dict
    :param tuned_profile: complete rendered yaml of tuned profile
        being used
    :type tuned_profile: str or None
    :param template: name of packaged template set,
        or path to user provided template set
    :type template: str or None
    :param output_path: proposed output path,
        if it does not exist, it will be created
    :type output_path: str or None
    :param output_filter: list of regular expressions to filter out
        which output files should be generated, if None, then all will
        be generated, based on selected template set
    :type output_filter: list[str] or None
    :param render_options: extra render options tuning
    :type render_options: RenderOptions
    :param write_profile_data: enables writing profile data used for
        templating to file in an output path, output path must be
        specified
    :type write_profile_data: bool
    :param extra_properties_data: pass in any specific key/values
        and call filter, the filter will override the values
    :type extra_properties_data: dict[str, str]

    :return: mapping of filename to generated data for further use
    :rtype: dict[str, str] or dict[str, unicode]
    """
    add_template_metadata(config_data)
    if render_options:
        add_render_config(config_data, render_options)

    if template is None:
        template = config_data.get("render", {}).get("template")
        LOG.debug(f"Profile specified template: {template}")
    if template is None:
        raise TemplateError(
            "Missing template. Neither user nor profile specifies a template."
        )

    try:
        env = get_template_environment(template)
    except TemplateError as exc:
        raise TemplateError(f"Failed to create template environment: {exc}")

    def override_value(value: str, value_key: str) -> str:
        """
        To work around some unexpected conversions by yaml loader
        for example empty string -> None and OFF -> False
        callers of yacfg need to pass in any specific key/values
        and call filter, the filter will override the values

        :param value: Value to override
        :type value: str
        :param value_key: Key of the value to override
        :type value_key: str
        :return: str
        """
        if extra_properties_data and value_key in extra_properties_data:
            return extra_properties_data[value_key]
        return value

    def empty_filter(value: str, value_key: str) -> str:
        """
        Simply pass the value

        :param value: Value to filter
        :type value: str
        :param value_key: Key of the value to filter
        :type value_key: str
        :return: str
        """
        # noinspection PyStatementEffect
        value_key
        return value

    def override_value_list_map_keys(
        value: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Replace keys with overrides if possible
        in list of maps
        :param value: Value to override
        :type value: list of dict
        :return: list of dict
        """
        return [override_value_map_keys(item) for item in value]

    def override_value_map_keys(value: Dict[str, Any]) -> Dict[str, Any]:
        """
        Replace keys with overrides if possible
        :param value: Value to override
        :type value: dict
        :return: dict
        """
        return {override_value(key, key): val for key, val in value.items()}

    # Pass empty filter for performance if extra_properties_data is not defined (no more conditions)
    env.filters["overridevalue"] = (
        override_value if extra_properties_data else empty_filter
    )
    env.filters["overridevalue_listmapkeys"] = (
        override_value_list_map_keys if extra_properties_data else empty_filter
    )

    template_list = get_main_template_list(env)
    if output_filter:
        template_list = filter_template_list(template_list, output_filter)

    LOG.debug(f"Config data:\n {yaml.dump(config_data, default_flow_style=False)}")

    if output_path and tuned_profile:
        ensure_output_path(output_path)
        if write_profile_data:
            write_output("profile_data.yaml", output_path, tuned_profile)

    return generate_outputs(config_data, template_list, env, output_path)


def generate(
    profile: str,
    template: Optional[str] = None,
    output_path: Optional[str] = None,
    output_filter: Optional[List[str]] = None,
    render_options: Optional[RenderOptions] = None,
    tuning_files_list: Optional[List[str]] = None,
    tuning_data_list: Optional[List[Dict[str, Any]]] = None,
    write_profile_data: bool = False,
    extra_properties_data: Optional[Dict[str, str]] = None,
) -> dict[str, str]:
    """Generate procedure using a list of tuning data

    generate_via_tuning_files output files based on output_filter, from
    the selected template set, with the selected profile, and write output to
    a proposed output path.

    :param profile: name of packaged profile,
        or path to user provided profile
    :type profile: str
    :param template: name of packaged template set,
        or path to user provided template set
    :type template: str | None
    :param output_path: proposed output path,
        if it does not exist, it will be created
    :type output_path: str | None
    :param output_filter: list of regular expressions to filter out
        which output files should be generated, if None, then all will
        be generated, based on the selected template set
    :type output_filter: list[str] | None
    :param render_options: extra render options tuning
    :type render_options: RenderOptions
    :param tuning_files_list: Additional yaml tuning files with tuning
        values.
    :type tuning_files_list: list[str] | None
    :param tuning_data_list: Additional user values to fine-tune the profile
        before applying it to the template.
    :type tuning_data_list: list[dict] | None
    :param write_profile_data: enables writing profile data used for
        templating to file in an output path, the output path must be
        specified
    :type write_profile_data: bool
    :param extra_properties_data: properties that can be used to help
        process templates with additional info
    :type extra_properties_data: dict[str, str]

    :return: mapping of filename to generated data for further use
    :rtype: dict[str, str] or dict[str, unicode]
    """

    config_data, tuned_profile = get_tuned_profile(
        profile=profile,
        tuning_files_list=tuning_files_list,
        tuning_data_list=tuning_data_list,
    )

    try:
        return generate_core(
            config_data=config_data,
            tuned_profile=tuned_profile,
            template=template,
            output_path=output_path,
            output_filter=output_filter,
            render_options=render_options,
            write_profile_data=write_profile_data,
            extra_properties_data=extra_properties_data,
        )
    except GenerationError as exc:
        LOG.error(f"Generation failed: {exc}")

    return {}  # Add a default return statement


# main alias
main = generate


def generate_outputs(
    config_data: Dict[str, Any],
    template_list: List[str],
    env: Environment,
    output_path: Optional[str] = None,
) -> Dict[str, str]:
    """Generate output files based on config_data, (filtered) template list,
    within the provided jinja environment, and if output_path is specified, then
    write results to that directory.

    .. note: output_path directory has to be created before.

    :param config_data: configuration data mapping for templating
    :type config_data: dict
    :param template_list: list of main template file names
    :type template_list: list[str]
    :param env: jinja2 template environment
    :type env: Environment
    :param output_path: path where to generate output files,
        or None to do a dry run
    :type output_path: str | None

    :raises GenerationError: when there was a problem with generating one of
        config files
    """
    result_data: Dict[str, str] = {}
    generate_exception: Optional[GenerationError] = None

    if output_path and not os.path.exists(output_path):
        raise GenerationError(f"Output path '{output_path}' does not exist.")

    for template_name in template_list:
        out_filename = get_output_filename(template_name)
        config_data["metadata"]["out_filename"] = template_name

        try:
            template: Template = env.get_template(template_name)
            output_data: str = template.render(config_data)

        except TemplateError as exc:
            LOG.error(f"Config file {out_filename} generation FAILED")
            LOG.exception("Original error")
            if not generate_exception:
                generate_exception = GenerationError(
                    f"There was a problem generating file {out_filename} with {template_name} template: {exc}"
                )
        else:
            LOG.debug(f"END {out_filename}")
            LOG.info(f"Config file {out_filename} generation PASSED")

            result_data[out_filename] = output_data

            if output_path:
                try:
                    write_output(out_filename, output_path, output_data)

                except Exception as exc:
                    LOG.error(
                        f"Failed to write output file {out_filename} to {output_path}"
                    )
                    LOG.exception("Write error")
                    generate_exception = GenerationError(
                        f"There was a problem writing output file '{out_filename}' to '{output_path}': {exc}"
                    )

    if generate_exception:
        raise generate_exception

    return result_data
