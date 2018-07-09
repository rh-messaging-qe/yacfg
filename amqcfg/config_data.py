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

import datetime
import time
from collections import namedtuple

from .meta import NAME


def add_template_metadata(config_data):
    """add templating metadata to original template data

    :param config_data:  original template data
    :type config_data: dict
    """
    now = datetime.datetime.now()

    config_data['metadata'] = {
        'tool_name': NAME,
        'datetime': {
            'datetime': now.strftime('%Y-%m-%d %H:%M'),
            'year': now.strftime('%Y'),
            'time': now.strftime('%H:%M'),
            'date': now.strftime('%Y-%m-%d'),
            'unix': time.time(),
        }
    }


def add_render_config(config_data, render_options):
    """add render related config to original template data

    :param config_data: original template data
    :type config_data: dict
    :param render_options: render options to tune up rendering
    :type render_options: RenderOptions
    """
    render_config = {}

    if render_options.generator_notice is not None:
        render_config['generator_notice'] = render_options.generator_notice
    if render_options.licenses is not None:
        render_config['licenses'] = render_options.licenses

    # update loaded config data
    if 'render' not in config_data:
        config_data['render'] = render_config
    else:
        config_data['render'].update(render_config)


RenderOptions = namedtuple('RenderOptions', ['generator_notice', 'licenses'])
