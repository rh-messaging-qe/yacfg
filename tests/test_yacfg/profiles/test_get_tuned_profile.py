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
import copy

import mock
import pytest
import yaml

import yacfg.profiles
from yacfg.exceptions import ProfileError
from yacfg.profiles import get_tuned_profile
from .fakes import fake_load_tuned_profile_no_defaults


@mock.patch('yacfg.profiles.load_tuning', mock.Mock())
@mock.patch('yacfg.profiles.load_profile_defaults', mock.Mock())
@mock.patch('yacfg.profiles.get_profile_template', mock.Mock())
def test_no_tuning(*_):
    profile_name = 'profile.yaml'
    tuning_data = None
    expected_data = fake_load_tuned_profile_no_defaults()

    # mock load_tuning
    yacfg.profiles.load_tuning.return_value = copy.deepcopy(expected_data[0])

    # mock load_profile_defaults
    yacfg.profiles.load_profile_defaults.return_value = expected_data[0]

    # simulating jinja profile rendering
    fake_profile = mock.Mock()
    fake_profile.name = profile_name
    yacfg.profiles.get_profile_template.return_value = fake_profile
    fake_profile.render.return_value = expected_data[1]

    profile_data = get_tuned_profile(profile_name, tuning_data)

    assert profile_data == expected_data

    # noinspection PyUnresolvedReferences
    yacfg.profiles.load_tuning.assert_called_with(
        profile_defaults=expected_data[0],
        tuning_data_list=None,
        tuning_files_list=None,
    )
    # noinspection PyUnresolvedReferences
    yacfg.profiles.load_profile_defaults.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    yacfg.profiles.get_profile_template.assert_called_with(profile_name)

    expected_data_render = copy.deepcopy(expected_data[0])
    expected_data_render['profile_path'] = profile_name
    fake_profile.render.assert_called_with(
        expected_data_render
    )


@mock.patch('yacfg.profiles.load_tuning', mock.Mock())
@mock.patch('yacfg.profiles.load_profile_defaults', mock.Mock())
@mock.patch('yacfg.profiles.get_profile_template', mock.Mock())
def test_tuning_data(*_):
    profile_name = 'profile.yaml'
    tuning_data = [{'a': 1}]
    expected_data = fake_load_tuned_profile_no_defaults()

    # mock load_tuning
    yacfg.profiles.load_tuning.return_value = copy.deepcopy(expected_data[0])

    # mock load_profile_defaults
    yacfg.profiles.load_profile_defaults.return_value = expected_data[0]

    # simulating jinja profile rendering
    fake_profile = mock.Mock()
    fake_profile.name = profile_name
    yacfg.profiles.get_profile_template.return_value = fake_profile
    fake_profile.render.return_value = expected_data[1]

    profile_data = get_tuned_profile(
        profile=profile_name,
        tuning_data_list=tuning_data,
    )

    assert profile_data == expected_data

    # noinspection PyUnresolvedReferences
    yacfg.profiles.load_tuning.assert_called_with(
        profile_defaults=expected_data[0],
        tuning_data_list=tuning_data,
        tuning_files_list=None,
    )
    # noinspection PyUnresolvedReferences
    yacfg.profiles.load_profile_defaults.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    yacfg.profiles.get_profile_template.assert_called_with(profile_name)

    expected_data_render = copy.deepcopy(expected_data[0])
    expected_data_render['profile_path'] = profile_name
    fake_profile.render.assert_called_with(
        expected_data_render
    )


@mock.patch('yacfg.profiles.load_tuning', mock.Mock())
@mock.patch('yacfg.profiles.load_profile_defaults', mock.Mock())
@mock.patch('yacfg.profiles.get_profile_template', mock.Mock())
def test_tuning_files_data(*_):
    profile_name = 'profile.yaml'
    tuning_data = [{'a': 1}]
    tuning_files = ['asdf.yaml']
    expected_data = fake_load_tuned_profile_no_defaults()

    # mock load_tuning
    yacfg.profiles.load_tuning.return_value = copy.deepcopy(expected_data[0])

    # mock load_profile_defaults
    yacfg.profiles.load_profile_defaults.return_value = expected_data[0]

    # simulating jinja profile rendering
    fake_profile = mock.Mock()
    fake_profile.name = profile_name
    yacfg.profiles.get_profile_template.return_value = fake_profile
    fake_profile.render.return_value = expected_data[1]

    profile_data = get_tuned_profile(
        profile=profile_name,
        tuning_files_list=tuning_files,
        tuning_data_list=tuning_data,
    )

    assert profile_data == expected_data

    # noinspection PyUnresolvedReferences
    yacfg.profiles.load_tuning.assert_called_with(
        profile_defaults=expected_data[0],
        tuning_data_list=tuning_data,
        tuning_files_list=tuning_files,
    )
    # noinspection PyUnresolvedReferences
    yacfg.profiles.load_profile_defaults.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    yacfg.profiles.get_profile_template.assert_called_with(profile_name)

    expected_data_render = copy.deepcopy(expected_data[0])
    expected_data_render['profile_path'] = profile_name
    fake_profile.render.assert_called_with(
        expected_data_render
    )


@mock.patch('yacfg.profiles.load_tuning', mock.Mock())
@mock.patch('yacfg.profiles.load_profile_defaults', mock.Mock())
@mock.patch('yacfg.profiles.get_profile_template', mock.Mock())
def test_tuning_files(*_):
    profile_name = 'profile.yaml'
    tuning_data = None
    tuning_files = ['asdf.yaml']
    expected_data = fake_load_tuned_profile_no_defaults()

    # mock load_tuning
    yacfg.profiles.load_tuning.return_value = copy.deepcopy(expected_data[0])

    # mock load_profile_defaults
    yacfg.profiles.load_profile_defaults.return_value = expected_data[0]

    # simulating jinja profile rendering
    fake_profile = mock.Mock()
    fake_profile.name = profile_name
    yacfg.profiles.get_profile_template.return_value = fake_profile
    fake_profile.render.return_value = expected_data[1]

    profile_data = get_tuned_profile(
        profile=profile_name,
        tuning_files_list=tuning_files,
        tuning_data_list=tuning_data,
    )

    assert profile_data == expected_data

    # noinspection PyUnresolvedReferences
    yacfg.profiles.load_tuning.assert_called_with(
        profile_defaults=expected_data[0],
        tuning_data_list=tuning_data,
        tuning_files_list=tuning_files,
    )
    # noinspection PyUnresolvedReferences
    yacfg.profiles.load_profile_defaults.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    yacfg.profiles.get_profile_template.assert_called_with(profile_name)

    expected_data_render = copy.deepcopy(expected_data[0])
    expected_data_render['profile_path'] = profile_name
    fake_profile.render.assert_called_with(
        expected_data_render
    )


@mock.patch('yacfg.profiles.load_profile_defaults',
            side_effect=ProfileError)
@mock.patch('yacfg.profiles.open',
            side_effect=('%this is not yaml',))
@mock.patch('yaml.load', mock.Mock())
@mock.patch('yacfg.profiles.get_profile_template', mock.Mock())
def test_bad_profile_exception(*_):
    profile_name = 'profile.yaml'
    tuning_files = ['bad']
    expected_data = 'key: value\n'

    # simulating jinja profile rendering
    fake_profile = mock.Mock()
    yacfg.profiles.get_profile_template.return_value = fake_profile
    fake_profile.render.return_value = expected_data

    with pytest.raises(ProfileError):
        get_tuned_profile(profile_name, tuning_files)

    # noinspection PyUnresolvedReferences
    yacfg.profiles.load_profile_defaults.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    yacfg.profiles.open.assert_not_called()
    # noinspection PyUnresolvedReferences
    yaml.load.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.profiles.get_profile_template.assert_not_called()
    fake_profile.render.assert_not_called()
