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

import ast
import copy
import json
import logging

import jinja2
from jinja2 import Environment, Template

from .config_data import add_template_metadata, add_render_config
from .exceptions import TemplateError, GenerationError
from .files import ensure_output_path, get_output_filename
from .output import write_output
from .profiles import get_tuned_profile
from .query import filter_template_list, get_main_template_list
from .templates import get_template_environment

# workaround for flake8: F401 'jinja2.Template' imported but unused
_t = Template
_e = Environment

LOG = logging.getLogger(__name__)


def generate_core(config_data, tuned_profile=None, template=None,
                  output_path=None, output_filter=None, render_options=None,
                  write_profile_data=False, extra_properties_data=None):
    """Core of the generator, gets complete dataset with selected
    template in config data or explicitly selected via template
    parameter at minimum, and generates outputs, if requested writes
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
        if do not exists, it will be created
    :type output_path: str or None
    :param output_filter: list of regular expressions to filter out
        which output files should be generated, if None, then all will
        be generated, based on selected template set
    :type output_filter: list[str] or None
    :param render_options: extra render options tuning
    :type render_options: RenderOptions
    :param write_profile_data: enables writing profile data used for
        templating to file in a output path, output path must be
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

    # template
    if template is None:
        template = config_data.get('render', {}).get('template')
        LOG.debug('Profile specified template: %s', template)
    if template is None:
        raise TemplateError(
            'Missing template. User nor profile specifies a template.'
        )

    env = get_template_environment(template)

    def override_value(value, value_key):
        """
        To work around some unexpected conversions by yaml loader
        for example empty string -> None and OFF -> False
        callers of yacfg need to pass in any specific key/values
        and call filter, the filter will override the values

        :param value:
        :type value: str
        :param value_key:
        :type value_key: str
        :return: str
        """
        if value_key in extra_properties_data:
            return extra_properties_data[value_key]
        return value

    def empty_filter(value, value_key):
        """
        Simply pass the value

        :param value:
        :type value: str
        :param value_key:
        :type value_key: str
        :return: str
        """
        return value

    def override_value_list_map_keys(value):
        """
        Replace keys with overrides if possible
        in list of maps
        :param value:
        :type value: list of dict
        :return: list of dict
        """
        for idx, item in enumerate(value):
            item = override_value_map_keys(item)
            value[idx] = item
        return value

    def override_value_map_keys(value):
        """
        Replace keys with overrides if possible
        :param value:
        :type value: dict
        :return: dict
        """
        new_map = dict()
        for key in value.keys():
            val = value[key]
            key = override_value(key, key)
            new_map[key] = val
        return new_map

    # Pass empty filter for performance if an extra_properties_data not defined (no more conditions)
    env.filters['overridevalue'] = override_value if extra_properties_data else empty_filter
    env.filters['overridevalue_listmapkeys'] = override_value_list_map_keys if extra_properties_data else empty_filter

    template_list = get_main_template_list(env)
    if output_filter:
        template_list = filter_template_list(template_list, output_filter)

    LOG.debug('Config data: %s', json.dumps(config_data))

    if output_path and tuned_profile:
        ensure_output_path(output_path)
        if write_profile_data:
            write_output('profile_data.yaml', output_path, tuned_profile)

    return generate_outputs(config_data, template_list, env, output_path)


def generate(profile, template=None, output_path=None,
             output_filter=None, render_options=None,
             tuning_files_list=None, tuning_data_list=None,
             write_profile_data=False, extra_properties_data=None):
    """Generate procedure using list of tuning data

    generate_via_tuning_files output files based on output_filter, from
    selected template set, with selected profile, and write output to
    a proposed output path.

    :param profile: name of packaged profile,
        or path to user provided profile
    :type profile: str
    :param template: name of packaged template set,
        or path to user provided template set
    :type template: str | None
    :param output_path: proposed output path,
        if do not exists, it will be created
    :type output_path: str | None
    :param output_filter: list of regular expressions to filter out
        which output files should be generated, if None, then all will
        be generated, based on selected template set
    :type output_filter: list[str] | None
    :param render_options: extra render options tuning
    :type render_options: RenderOptions
    :param tuning_files_list: Additional yaml tuning files with tuning
        values.
    :type tuning_files_list: list[str] | None
    :param tuning_data_list: Additional user values to fine-tune profile
        before applying it to template.
    :type tuning_data_list: list[dict] | None
    :param write_profile_data: enables writing profile data used for
        templating to file in a output path, output path must be
        specified
    :type write_profile_data: bool
    :param extra_properties_data: properties that can be used to help
        process templates with additional info
    :type extra_properties_data: dict[str,str]

    :return: mapping of filename to generated data for further use
    :rtype: dict[str, str] or dict[str, unicode]
    """

    config_data, tuned_profile = get_tuned_profile(
        profile=profile,
        tuning_files_list=tuning_files_list,
        tuning_data_list=tuning_data_list,
    )

    return generate_core(
        config_data=config_data,
        tuned_profile=tuned_profile,
        template=template,
        output_path=output_path,
        output_filter=output_filter,
        render_options=render_options,
        write_profile_data=write_profile_data,
        extra_properties_data=extra_properties_data
    )


# main alias
main = generate


def generate_outputs(config_data, template_list, env, output_path=None):
    """Generate output files based on config_data, (filtered) template list,
    within provided jinja environment, and if output_path is specified, then
    write results to that directory.

    .. note: output_path directory has to be created before.

    :param config_data: configuration data mapping for templating
    :type config_data: dict
    :param template_list: list of main template file names
    :type template_list: list[str]
    :param env: jinja2 template environment
    :type env: Environment
    :param output_path: path where to generate_via_tuning_files output files,
        or None to do a dry run
    :type output_path: str

    :raises GenerationError: when there was a problem with generating one of
        config files

    :return: mapping of filename to generated data for further use
    :rtype: dict[str, str] or dict[str, unicode]
    """
    generate_exception = None
    result_data = {}

    # only additions of runtime data happens on base level,
    # so deeper structures are unaffected
    config_data = copy.copy(config_data)

    # metadata structure initialization,
    # if called without add_template_metadata()
    if 'metadata' not in config_data:
        config_data['metadata'] = {}

    for template_name in template_list:
        out_filename = get_output_filename(template_name)
        config_data['metadata']['out_filename'] = template_name

        try:
            template = env.get_template(template_name)
            output_data = template.render(config_data)
        except jinja2.TemplateError as exc:
            LOG.error('Config file "%s" generation FAILED', out_filename)
            LOG.exception('Original error')
            if not generate_exception:
                generate_exception = GenerationError(
                    'There was a problem generating file "%s" with "%s" '
                    'template: %s'
                    % (out_filename, template_name, exc)
                )
        else:
            LOG.debug('BEGIN %s\n%s', out_filename, output_data)
            LOG.debug('END %s' % out_filename)
            LOG.info('Config file "%s" generation PASSED', out_filename)

            result_data[out_filename] = output_data

            if output_path:
                write_output(out_filename, output_path, output_data)

    if generate_exception:
        raise generate_exception

    return result_data
