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

import jinja2
from jinja2 import Environment, FileSystemLoader

from .exceptions import TemplateError
from .files import get_templates_path, select_template_dir

LOG = logging.getLogger(__name__)


def get_template_environment(template_name):
    """Create jinja2 environment for selected template

    :param template_name: name of template set
        (alternatively path to user specified template set)
    :type template_name: str

    :return: jinja2 environment
    :rtype: Environment
    """
    templates_path = get_templates_path()

    selected_template_path = select_template_dir(template_name)

    try:
        env = Environment(
            loader=FileSystemLoader([
                selected_template_path,  # selected template
                templates_path,  # all templates for includes
            ]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
    except jinja2.TemplateError:
        LOG.exception('Original Error')
        # this is yacfg.exceptions.TemplateError
        raise TemplateError(
            'There was a problem with templating environment.'
        )

    return env
