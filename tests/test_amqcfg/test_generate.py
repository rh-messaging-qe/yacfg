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
from yacfg.yacfg import generate
from yacfg.exceptions import ProfileError, TemplateError
from .profiles.fakes import (
    fake_load_tuned_profile_no_defaults,
    fake_load_tuned_profile_w_template
)


@mock.patch('yacfg.yacfg.get_tuned_profile',
            side_effect=fake_load_tuned_profile_no_defaults)
@mock.patch('yacfg.yacfg.add_template_metadata', mock.Mock())
@mock.patch('yacfg.yacfg.add_render_config', mock.Mock())
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_render_options(*_):
    profile = 'profile.yaml'
    template = 'template/1.0.0'
    render_options = 'Render options'
    expected_result = 'generated data'

    config_data, _ = fake_load_tuned_profile_no_defaults()

    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate(
        profile=profile,
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


@mock.patch('yacfg.yacfg.get_tuned_profile', mock.Mock())
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_tuning_files(*_):
    profile = 'profile.yaml'
    template = 'template/1.0.0'
    tuning_files = ['tune1.yaml', 'tune2.yaml']
    expected_result = 'generated data'

    yacfg.yacfg.get_tuned_profile.side_effect = \
        fake_load_tuned_profile_no_defaults
    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate(
        profile=profile,
        template=template,
        tuning_files_list=tuning_files,
    )

    assert expected_result == result

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_tuned_profile.assert_called_with(
        profile=profile,
        tuning_files_list=tuning_files,
        tuning_data_list=None,
    )
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


@mock.patch('yacfg.yacfg.get_tuned_profile',
            side_effect=fake_load_tuned_profile_no_defaults)
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_tuning_data(*_):
    profile = 'profile.yaml'
    template = 'template/1.0.0'
    tuning_data = [
        {'a': '1'},
        {'b': '2'},
    ]
    expected_result = 'generated data'

    yacfg.yacfg.get_tuned_profile.side_effect = \
        fake_load_tuned_profile_no_defaults
    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate(
        profile=profile,
        template=template,
        tuning_data_list=tuning_data,
    )

    assert expected_result == result

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.get_tuned_profile.assert_called_with(
        profile=profile,
        tuning_files_list=None,
        tuning_data_list=tuning_data,
    )
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


@mock.patch('yacfg.yacfg.get_tuned_profile',
            side_effect=fake_load_tuned_profile_no_defaults)
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_no_output_path_write_profile(*_):
    profile = 'profile.yaml'
    template = 'template/1.0.0'
    expected_result = 'generated data'

    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate(
        profile=profile,
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


@mock.patch('yacfg.yacfg.get_tuned_profile',
            side_effect=fake_load_tuned_profile_no_defaults)
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_output_path_write_profile(*_):
    profile = 'profile.yaml'
    template = 'template/1.0.0'
    output_path = '/out/directory'
    expected_result = 'generated data'

    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate(
        profile=profile,
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


@mock.patch('yacfg.yacfg.get_tuned_profile',
            side_effect=fake_load_tuned_profile_no_defaults)
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_output_path(*_):
    profile = 'profile.yaml'
    template = 'template/1.0.0'
    output_path = '/out/directory'
    expected_result = 'generated data'

    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate(
        profile=profile,
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


@mock.patch('yacfg.yacfg.get_tuned_profile',
            side_effect=fake_load_tuned_profile_no_defaults)
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_template(*_):
    profile = 'profile.yaml'
    template = 'template/1.0.0'
    expected_result = 'generated data'

    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate(
        profile=profile,
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


@mock.patch('yacfg.yacfg.get_tuned_profile',
            side_effect=fake_load_tuned_profile_w_template)
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_true_profile_template(*_):
    profile = 'profile.yaml'
    expected_result = 'generated data'

    yacfg.yacfg.generate_outputs.return_value = expected_result

    result = generate(profile=profile)

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


@mock.patch('yacfg.yacfg.get_tuned_profile',
            side_effect=fake_load_tuned_profile_no_defaults)
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_no_template_exception(*_):
    profile = 'profile.yaml'

    with pytest.raises(TemplateError):
        generate(profile=profile)

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


@mock.patch('yacfg.yacfg.get_tuned_profile', side_effect=ProfileError)
@mock.patch('yacfg.yacfg.get_template_environment', mock.Mock())
@mock.patch('yacfg.yacfg.get_main_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.filter_template_list', mock.Mock())
@mock.patch('yacfg.yacfg.ensure_output_path', mock.Mock())
@mock.patch('yacfg.yacfg.write_output', mock.Mock())
@mock.patch('yacfg.yacfg.generate_outputs', mock.Mock())
def test_bad_profile_exception(*_):
    profile = 'bad_profile.yaml'

    with pytest.raises(ProfileError):
        generate(profile=profile)

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
