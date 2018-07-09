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
import yaml

import amqcfg.profiles
from amqcfg.exceptions import ProfileError
from amqcfg.profiles import get_tuned_profile


@mock.patch('amqcfg.profiles.load_profile_defaults',
            side_effect=({'var': 'value'},))
@mock.patch('amqcfg.profiles.open', mock.MagicMock())
@mock.patch('yaml.load', mock.Mock())
@mock.patch('amqcfg.profiles.get_profile_template', mock.Mock())
def test_no_tuning(*_):
    profile_name = 'profile.yaml'
    tuning_files = None
    expected_data = 'key: value\n'

    # simulating jinja profile rendering
    fake_profile = mock.Mock()
    amqcfg.profiles.get_profile_template.return_value = fake_profile
    fake_profile.render.return_value = expected_data

    profile_data = get_tuned_profile(profile_name, tuning_files)

    assert profile_data == expected_data
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.load_profile_defaults.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    yaml.load.assert_not_called()
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.open.assert_not_called()
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.get_profile_template.assert_called_with(profile_name)
    fake_profile.render.assert_called_with(
        {'var': 'value'}
    )


@mock.patch('amqcfg.profiles.load_profile_defaults',
            side_effect=({'var': 'value'},))
@mock.patch('amqcfg.profiles.open', mock.MagicMock())
@mock.patch('yaml.load', side_effect=({'a': 1}, {'b': 2},))
@mock.patch('amqcfg.profiles.get_profile_template', mock.Mock())
def test_tuning(*_):
    profile_name = 'profile.yaml'
    tuning_files = ['a', 'b']
    expected_data = 'key: value\n'

    # simulating jinja profile rendering
    fake_profile = mock.Mock()
    amqcfg.profiles.get_profile_template.return_value = fake_profile
    fake_profile.render.return_value = expected_data

    profile_data = get_tuned_profile(profile_name, tuning_files)

    assert profile_data == expected_data
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.load_profile_defaults.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    yaml.load.assert_called()
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.open.assert_has_calls([
        mock.call('a', 'r'), mock.call('b', 'r')
    ])
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.get_profile_template.assert_called_with(profile_name)
    fake_profile.render.assert_called_with(
        {'var': 'value', 'a': 1, 'b': 2}
    )


@mock.patch('amqcfg.profiles.load_profile_defaults',
            side_effect=({'var': 'value'},))
@mock.patch('amqcfg.profiles.open',
            side_effect=IOError)
@mock.patch('yaml.load', mock.Mock())
@mock.patch('amqcfg.profiles.get_profile_template', mock.Mock())
def test_bad_file_exception(*_):
    profile_name = 'profile.yaml'
    tuning_files = ['bad']
    expected_data = 'key: value\n'

    # simulating jinja profile rendering
    fake_profile = mock.Mock()
    amqcfg.profiles.get_profile_template.return_value = fake_profile
    fake_profile.render.return_value = expected_data

    with pytest.raises(ProfileError):
        get_tuned_profile(profile_name, tuning_files)

    # noinspection PyUnresolvedReferences
    amqcfg.profiles.load_profile_defaults.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    yaml.load.assert_not_called()
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.open.assert_called()
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.get_profile_template.assert_not_called()
    fake_profile.render.assert_not_called()


@mock.patch('amqcfg.profiles.load_profile_defaults',
            side_effect=ProfileError)
@mock.patch('amqcfg.profiles.open',
            side_effect=('%this is not yaml',))
@mock.patch('yaml.load', mock.Mock())
@mock.patch('amqcfg.profiles.get_profile_template', mock.Mock())
def test_bad_profile_exception(*_):
    profile_name = 'profile.yaml'
    tuning_files = ['bad']
    expected_data = 'key: value\n'

    # simulating jinja profile rendering
    fake_profile = mock.Mock()
    amqcfg.profiles.get_profile_template.return_value = fake_profile
    fake_profile.render.return_value = expected_data

    with pytest.raises(ProfileError):
        get_tuned_profile(profile_name, tuning_files)

    # noinspection PyUnresolvedReferences
    amqcfg.profiles.load_profile_defaults.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.open.assert_not_called()
    # noinspection PyUnresolvedReferences
    yaml.load.assert_not_called()
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.get_profile_template.assert_not_called()
    fake_profile.render.assert_not_called()


@mock.patch('amqcfg.profiles.load_profile_defaults',
            side_effect=({'var': 'value'},))
@mock.patch('amqcfg.profiles.open',
            side_effect=('%this is not yaml',))
# @mock.patch('yaml.load', mock.Mock())
@mock.patch('amqcfg.profiles.get_profile_template', mock.Mock())
def test_bad_yaml_data(*_):
    profile_name = 'profile.yaml'
    tuning_files = ['bad']
    expected_data = 'key: value\n'

    # simulating jinja profile rendering
    fake_profile = mock.Mock()
    amqcfg.profiles.get_profile_template.return_value = fake_profile
    fake_profile.render.return_value = expected_data

    with pytest.raises(ProfileError):
        get_tuned_profile(profile_name, tuning_files)

    # noinspection PyUnresolvedReferences
    amqcfg.profiles.load_profile_defaults.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.open.assert_called()
    # noinspection PyUnresolvedReferences
    amqcfg.profiles.get_profile_template.assert_not_called()
    fake_profile.render.assert_not_called()
