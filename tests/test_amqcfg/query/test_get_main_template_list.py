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

import mock

from yacfg.query import get_main_template_list


def fake_list_templates(filter_func):
    file_list = [
        'broker.xml.jinja2',
        'artemis-users.properties.jinja2',
        'not_a_template.xml',
    ]
    return [i for i in file_list if filter_func(i)]


def test_basic(*_):
    expected = [
        'broker.xml.jinja2',
        'artemis-users.properties.jinja2',
    ]
    env = mock.Mock()
    env.list_templates = fake_list_templates

    result = get_main_template_list(env)
    assert expected == result
