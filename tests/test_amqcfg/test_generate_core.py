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
import pytest

import yacfg.yacfg
from yacfg.yacfg import generate_core
from yacfg.exceptions import TemplateError
from .profiles.fakes import (
    fake_load_tuned_profile_no_defaults,
    fake_load_tuned_profile_w_template
)


@mock.patch('yacfg.yacfg.add_template_metadata', mock.Mock())
@mock.patch('yacfg.yacfg.add_render_config', mock.Mock())
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true(*_):
    template = 'template/1.0.0'
    render_options = 'Render options'
    expected_result = 'generated data'

    config_data, _ = fake_load_tuned_profile_no_defaults()

    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate_core(
        config_data=config_data,
        template=template,
        render_options=render_options
    )

    assert expected_result == result

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.add_render_config.assert_called_with(config_data,
                                                     render_options)
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_template_environment.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_main_template_list.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.filter_template_list.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.ensure_output_path.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.generate_outputs.assert_called()


@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_no_output_path_write_profile(*_):
    template = 'template/1.0.0'
    expected_result = 'generated data'

    config_data, tuned_profile = fake_load_tuned_profile_no_defaults()
    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate_core(
        config_data=config_data,
        tuned_profile=tuned_profile,
        template=template,
        write_profile_data=True,
    )

    assert expected_result == result

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_template_environment.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_main_template_list.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.filter_template_list.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.ensure_output_path.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.generate_outputs.assert_called()


@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_output_path_write_no_profile(*_):
    template = 'template/1.0.0'
    expected_result = 'generated data'

    config_data, _ = fake_load_tuned_profile_no_defaults()
    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate_core(
        config_data=config_data,
        template=template,
        write_profile_data=True,
    )

    assert expected_result == result

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_template_environment.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_main_template_list.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.filter_template_list.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.ensure_output_path.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.generate_outputs.assert_called()


@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_output_path_write_profile(*_):
    template = 'template/1.0.0'
    output_path = '/out/directory'
    expected_result = 'generated data'

    config_data, tuned_profile = fake_load_tuned_profile_no_defaults()
    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate_core(
        config_data=config_data,
        tuned_profile=tuned_profile,
        template=template,
        output_path=output_path,
        write_profile_data=True,
    )

    assert expected_result == result

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_template_environment.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_main_template_list.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.filter_template_list.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.ensure_output_path.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.generate_outputs.assert_called()


@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_output_path(*_):
    template = 'template/1.0.0'
    output_path = '/out/directory'
    expected_result = 'generated data'

    config_data, tuned_profile = fake_load_tuned_profile_no_defaults()
    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate_core(
        config_data=config_data,
        tuned_profile=tuned_profile,
        template=template,
        output_path=output_path,
    )

    assert expected_result == result

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_template_environment.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_main_template_list.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.filter_template_list.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.ensure_output_path.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.generate_outputs.assert_called()


@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_template(*_):
    template = 'template/1.0.0'
    expected_result = 'generated data'

    config_data, _ = fake_load_tuned_profile_no_defaults()
    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate_core(
        config_data=config_data,
        template=template,
    )

    assert expected_result == result

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_template_environment.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_main_template_list.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.filter_template_list.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.ensure_output_path.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.generate_outputs.assert_called()


@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_profile_template(*_):
    expected_result = 'generated data'

    config_data, _ = fake_load_tuned_profile_w_template()
    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate_core(config_data=config_data)

    assert expected_result == result

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_template_environment.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_main_template_list.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.filter_template_list.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.ensure_output_path.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.generate_outputs.assert_called()


@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_no_template_exception(*_):
    config_data, _ = fake_load_tuned_profile_no_defaults()

    with pytest.raises(TemplateError):
        generate_core(config_data=config_data)

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_template_environment.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_main_template_list.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.filter_template_list.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.ensure_output_path.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.write_output.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.yacfg.generate_outputs.assert_not_called()
