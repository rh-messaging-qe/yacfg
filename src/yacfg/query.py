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
import posixpath
import re

from .files import get_module_path
from .meta import TEMPLATES, PROFILES

LOG = logging.getLogger(__name__)


def filter_template_list(template_list, output_filter):
    """Based on list of output filters, select templates to be generated

    :param template_list: list of template file names
    :type template_list: list[str]
    :param output_filter: list of regular expressions to filter out templates
    :type output_filter: list[str]
    :return: list of selected template file names to process
    :rtype: list[str]
    """
    output_filter = [re.compile(flt) for flt in output_filter]
    template_list = [
        templ
        for templ in template_list
        for rex in output_filter if rex.match(templ)
    ]
    LOG.debug('Filtered template files list: %s', template_list)
    return template_list


def list_templates():
    """List all packaged templates with their package relative path

    Package is directory under 'templates' directory that contains
    file named '_template'. It would be good if template directory
    would contain some jinja2 templates.

    :return: list of templates paths from package
    :rtype: list[str]
    """
    module_path = get_module_path()

    templates_path = os.path.join(module_path, TEMPLATES)
    result = []

    for root, subdirs, files in os.walk(templates_path):
        for fn in files:
            if fn == '_template':
                prefix_path = os.path.relpath(root, templates_path)
                result.append(prefix_path)
                break

    result = [posixpath.join(*i.split(os.path.sep)) for i in result]

    return result


def list_profiles():
    """List all packaged complete profiles with their package relative path.

    Profile is any yaml file under 'profiles' directory in package, that is
    not placed under directory with leading underscore like _modules

    :return: list of profile from package
    :rtype: list[str]
    """
    module_path = get_module_path()
    profiles_path = os.path.join(module_path, PROFILES)

    result = []
    for root, _, files in os.walk(profiles_path):
        prefix_path = os.path.relpath(root, profiles_path)
        # skip over underscored paths
        path_levels = prefix_path.split(os.path.sep)
        if any([x.startswith('_') for x in path_levels]):
            continue
        # filter only yaml profiles
        tmp_files = [
            fn
            for fn in files if (
                fn.endswith('.yaml')
                or fn.endswith('.jinja2')
                or fn.endswith('.j2')
            )
        ]
        # add relative profile path if it is not profiles root,
        # it would add './' which is undesirable
        if prefix_path != '.':
            tmp_files = [
                os.path.join(prefix_path, fn)
                for fn in tmp_files
            ]
        result += tmp_files

    result = [posixpath.join(*i.split(os.path.sep)) for i in result]

    return result


def get_main_template_list(env):
    """Get list of main templates from selected template set

    .. note: main template -> template that resembles a output config file

    :param env: jinja2 environment
    :type env: Environment

    :return: list of main template names
    :rtype: list[str]
    """
    rex_main_template = re.compile(r'^[^/]+\.jinja2$')

    def main_template_filter(name):
        return rex_main_template.match(name)

    templ_list = env.list_templates(filter_func=main_template_filter)

    LOG.debug('Main template files list: %s', templ_list)

    return templ_list
