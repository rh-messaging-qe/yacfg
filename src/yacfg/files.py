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

import logging
import os
import re

from .exceptions import ProfileError, TemplateError
from .meta import PROFILES, TEMPLATES

LOG = logging.getLogger(__name__)

REX_TEMPLATE_TO_OUTPUT = re.compile(r'^(.*)(\.jinja2)$')


def get_module_path():
    """Get module installation path,
    for reading packaged template sets and profiles

    :return: module installation path
    :rtype: str
    """
    module_path = os.path.dirname(__file__)
    LOG.debug('Module path: %s', module_path)
    return module_path


def get_profiles_path():
    """Helper for getting profiles path from module installation location

    :return: path to packaged profiles directory
    :rtype: str
    """
    module_path = get_module_path()
    profiles_path = os.path.join(module_path, PROFILES)
    return profiles_path


def get_templates_path():
    """Helper for getting templates path from module installation location

    :return: path packaged templates directory
    :rtype: str
    """
    module_path = get_module_path()
    templates_path = os.path.join(module_path, TEMPLATES)
    return templates_path


def select_profile_file(profile_name):
    """Select profile path and filename (user defined or from package)

    :param profile_name: profile name, from package or filename from user
    :type profile_name: str

    :raises ProfileError: when requested profile file does not exists

    :return: selected path to profile and profile name
    :rtype: tuple[str, str]
    """
    profiles_path = get_profiles_path()
    selected_template_path = profiles_path
    selected_template_name = profile_name

    user_extra_path = os.path.join(PROFILES, profile_name)
    if os.path.isfile(user_extra_path):  # user path omitting 'profile' dir
        profile_tmp_name = os.path.abspath(user_extra_path)
        selected_template_path = os.path.dirname(profile_tmp_name)
        selected_template_name = os.path.basename(profile_tmp_name)
        LOG.debug('Using user defined template path "%s"', profile_tmp_name)

    if os.path.isfile(profile_name):  # user direct path
        profile_tmp_name = os.path.abspath(profile_name)
        selected_template_path = os.path.dirname(profile_tmp_name)
        selected_template_name = os.path.basename(profile_tmp_name)
        LOG.debug('Using user defined template path "%s"', profile_tmp_name)

    complete_path = os.path.join(selected_template_path,
                                 selected_template_name)
    if not os.path.isfile(complete_path):
        raise ProfileError(
            'Unable to find a requested profile "%s"' % profile_name
        )
    return selected_template_name, selected_template_path


def select_template_dir(template_name):
    """Select template dir path (user defined or packaged)

    :param template_name: template name, from package, or dirname from user
    :type template_name: str

    :raises TemplateError: when requested template does not exists

    :return: selected path to template dir
    :rtype: str
    """
    templates_path = get_templates_path()
    selected_template_path = os.path.join(templates_path, template_name)
    user_extra_path = os.path.join(TEMPLATES, template_name)
    if os.path.isdir(user_extra_path):
        selected_template_path = user_extra_path
        LOG.debug('Using user defined template path "%s"', template_name)
    if os.path.isdir(template_name):
        selected_template_path = template_name
        LOG.debug('Using user defined template path "%s"', template_name)

    if not os.path.isdir(selected_template_path):
        raise TemplateError(
            'Unable to load requested template set "%s"' % template_name
        )

    if not os.path.isfile(os.path.join(selected_template_path, '_template')):
        raise TemplateError(
            'Selected template "%s" does not contain'
            ' "_template" file, so it is not considered a template'
        )
    LOG.debug('Selected template: %s', selected_template_path)
    return selected_template_path


def ensure_output_path(output_path):
    """Ensure that output path is actually existing directory

    :param output_path: selected output path to ensure
    :type output_path: str

    :raises OSError: if output_path exists but it is not a directory
    """
    if not os.path.isdir(output_path):
        if os.path.isfile(output_path):
            raise IOError(
                'Output path "%s" already exists and it is not a directory!'
                % output_path
            )
        os.makedirs(output_path, exist_ok=True)
        LOG.debug('Created directory "%s"', output_path)
    else:
        LOG.debug('Requested directory "%s" exists', output_path)


def get_output_filename(template_name):
    """Process a template filename and get output file name

    .. note: removing '.jinja2' suffix

    :param template_name: filename of a template
    :type template_name: str

    :return: output filename based on template name
    :rtype: str
    """
    match = REX_TEMPLATE_TO_OUTPUT.match(template_name)
    output_filename = template_name
    if match:
        output_filename = match.group(1)

    return output_filename
