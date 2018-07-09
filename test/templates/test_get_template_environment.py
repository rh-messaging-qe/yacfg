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

import jinja2
import mock
import pytest

import amqcfg.exceptions
import amqcfg.templates
from amqcfg.templates import get_template_environment
from ..files.fakes import fake_select_template_dir
from ..files.fakes import fake_templates_path


@mock.patch('amqcfg.templates.get_templates_path',
            side_effect=fake_templates_path)
@mock.patch('amqcfg.templates.select_template_dir',
            side_effect=fake_select_template_dir)
@mock.patch('amqcfg.templates.FileSystemLoader', mock.Mock())
@mock.patch('amqcfg.templates.Environment', mock.Mock())
def test_true(*_):
    template_name = 'template/1.0.0'
    expected_env = 'template environment'
    expected_template_path = fake_templates_path()
    expected_selected_templates = fake_select_template_dir(template_name)

    amqcfg.templates.Environment.return_value = expected_env

    result = get_template_environment(template_name)

    assert expected_env == result

    # noinspection PyUnresolvedReferences
    amqcfg.templates.select_template_dir.assert_called_with(template_name)
    # noinspection PyUnresolvedReferences
    amqcfg.templates.FileSystemLoader.assert_called_with([
        expected_selected_templates, expected_template_path
    ])


@mock.patch('amqcfg.templates.get_templates_path',
            side_effect=fake_templates_path)
@mock.patch('amqcfg.templates.select_template_dir',
            side_effect=fake_select_template_dir)
@mock.patch('amqcfg.templates.FileSystemLoader',
            side_effect=jinja2.TemplateError)
@mock.patch('amqcfg.templates.Environment', mock.Mock())
def test_jinja_loader_exception(*_):
    template_name = 'template/1.0.0'
    expected_env = 'template environment'

    amqcfg.templates.Environment.return_value = expected_env

    # jinja2 also have a TemplateError exception
    with pytest.raises(amqcfg.exceptions.TemplateError):
        get_template_environment(template_name)


@mock.patch('amqcfg.templates.get_templates_path',
            side_effect=fake_templates_path)
@mock.patch('amqcfg.templates.select_template_dir',
            side_effect=fake_select_template_dir)
@mock.patch('amqcfg.templates.FileSystemLoader', mock.Mock())
@mock.patch('amqcfg.templates.Environment', side_effect=jinja2.TemplateError)
def test_jinja_environment_exception(*_):
    template_name = 'template/1.0.0'
    expected_env = 'template environment'

    amqcfg.templates.Environment.return_value = expected_env

    # jinja2 also have a TemplateError exception
    with pytest.raises(amqcfg.exceptions.TemplateError):
        get_template_environment(template_name)
