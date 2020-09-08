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

import yacfg.yacfg
from yacfg.yacfg import generate_outputs
from yacfg.exceptions import GenerationError


@mock.patch('yacfg.yacfg.write_output', mock.Mock())
def test_one_true_no_output(*_):
    config_data = {}
    template_list = [
        'broker.xml.jinja2',
    ]

    expected_result_data = {
        'broker.xml': 'Rendered data'
    }

    env = mock.Mock()
    template = mock.Mock()
    env.get_template.return_value = template
    template.render.return_value = 'Rendered data'

    # noinspection PyTypeChecker
    result = generate_outputs(
        config_data=config_data,
        template_list=template_list,
        env=env,
        output_path=None
    )

    assert expected_result_data == result

    env.get_template.assert_called_with('broker.xml.jinja2')
    template.render.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_not_called()


@mock.patch('yacfg.yacfg.write_output', mock.Mock())
def test_one_true_output(*_):
    config_data = {}
    output_file = 'broker.xml'
    output_path = '/output/directory'
    expected_output_data = 'Rendered data'
    template_list = [
        '%s.jinja2' % output_file,
    ]
    expected_result_data = {
        output_file: 'Rendered data'
    }

    env = mock.Mock()
    template = mock.Mock()
    env.get_template.return_value = template
    template.render.return_value = expected_output_data

    # noinspection PyTypeChecker
    result = generate_outputs(
        config_data=config_data,
        template_list=template_list,
        env=env,
        output_path=output_path
    )

    assert expected_result_data == result

    env.get_template.assert_called_with('broker.xml.jinja2')
    template.render.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_called_with(output_file, output_path,
                                                expected_output_data)


@mock.patch('yacfg.yacfg.write_output', mock.Mock())
def test_one_exception_render(*_):
    config_data = {}
    output_file = 'broker.xml'
    output_path = '/output/directory'
    template_list = [
        '%s.jinja2' % output_file,
    ]

    env = mock.Mock()
    template = mock.Mock()
    env.get_template.return_value = template
    template.render.side_effect = jinja2.TemplateError

    with pytest.raises(GenerationError):
        # noinspection PyTypeChecker
        generate_outputs(
            config_data=config_data,
            template_list=template_list,
            env=env,
            output_path=output_path
        )

    env.get_template.assert_called_with('broker.xml.jinja2')
    template.render.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_not_called()


@mock.patch('yacfg.yacfg.write_output', mock.Mock())
def test_one_exception_template(*_):
    config_data = {}
    output_file = 'broker.xml'
    output_path = '/output/directory'
    template_list = [
        '%s.jinja2' % output_file,
    ]

    env = mock.Mock()
    env.get_template.side_effect = jinja2.TemplateError

    with pytest.raises(GenerationError):
        # noinspection PyTypeChecker
        generate_outputs(
            config_data=config_data,
            template_list=template_list,
            env=env,
            output_path=output_path
        )

    env.get_template.assert_called_with('broker.xml.jinja2')
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_not_called()
