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

import pytest
import amqcfg.config_data

dataset_render_config = (
    (amqcfg.config_data.RenderOptions(None, None), 'generator_notice', None),
    (amqcfg.config_data.RenderOptions(None, None), 'licenses', None),
    (amqcfg.config_data.RenderOptions(True, None), 'generator_notice', True),
    (amqcfg.config_data.RenderOptions(False, None), 'generator_notice', False),
    (amqcfg.config_data.RenderOptions(None, True), 'licenses', True),
    (amqcfg.config_data.RenderOptions(None, False), 'licenses', False),
)


@pytest.mark.parametrize('render_options,key,value', dataset_render_config)
def test_add_render_config_members(render_options, key, value):
    data = {}
    amqcfg.config_data.add_render_config(config_data=data,
                                         render_options=render_options)
    if value is not None:
        assert key in data['render']
    else:
        assert key not in data['render']


@pytest.mark.parametrize('render_options,key,value', dataset_render_config)
def test_add_render_config_values(render_options, key, value):
    data = {}
    amqcfg.config_data.add_render_config(config_data=data,
                                         render_options=render_options)
    if value is not None:
        assert data['render'][key] == value
    else:
        assert True
