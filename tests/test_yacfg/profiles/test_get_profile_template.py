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

import yacfg.profiles
from yacfg.exceptions import TemplateError
from yacfg.profiles import get_profile_template
from ..files.fakes import fake_select_profile_file, fake_profile_path


@mock.patch('yacfg.profiles.select_profile_file',
            side_effect=fake_select_profile_file)
@mock.patch('os.path.isdir', side_effect=(True,))
@mock.patch('yacfg.profiles.get_profiles_path',
            side_effect=fake_profile_path)
@mock.patch('yacfg.profiles.FileSystemLoader', mock.Mock())
@mock.patch('yacfg.profiles.Environment', mock.Mock())
def test_true(*_):
    profile_name = 'profile.yaml'
    expected_template = 'my_template'
    expected_selected_name, expected_selected_path = \
        fake_select_profile_file(profile_name)

    fake_env = mock.Mock()
    yacfg.profiles.Environment.return_value = fake_env
    fake_env.get_template.return_value = expected_template

    template = get_profile_template(profile_name)

    assert template == expected_template
    # noinspection PyUnresolvedReferences
    yacfg.profiles.select_profile_file.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    yacfg.profiles.FileSystemLoader.assert_called_with([
        expected_selected_path,
        fake_profile_path()
    ])
    fake_env.get_template.assert_called_with(expected_selected_name)


@mock.patch('yacfg.profiles.select_profile_file',
            side_effect=fake_select_profile_file)
@mock.patch('os.path.isdir', side_effect=(False,))
@mock.patch('yacfg.profiles.get_profiles_path',
            side_effect=fake_profile_path)
@mock.patch('yacfg.profiles.FileSystemLoader', mock.Mock())
@mock.patch('yacfg.profiles.Environment', mock.Mock())
def test_bad_profile_exception(*_):
    profile_name = 'bad_profile.yaml'
    expected_template = 'my_template'

    fake_env = mock.Mock()
    yacfg.profiles.Environment.return_value = fake_env
    fake_env.get_template.return_value = expected_template

    with pytest.raises(TemplateError):
        get_profile_template(profile_name)

    # noinspection PyUnresolvedReferences
    yacfg.profiles.select_profile_file.assert_called_with(profile_name)
    # noinspection PyUnresolvedReferences
    yacfg.profiles.FileSystemLoader.assert_not_called()
    fake_env.get_template.assert_not_called()
