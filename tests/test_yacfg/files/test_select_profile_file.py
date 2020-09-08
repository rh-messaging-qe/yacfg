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

import os

import mock
import pytest

import yacfg.files
import yacfg.meta
from yacfg.exceptions import ProfileError
from .fakes import fake_module_path, fake_profile_path, fake_os_abspath


@mock.patch('yacfg.files.get_module_path', side_effect=fake_module_path)
@mock.patch('os.path.isfile', side_effect=(False, False, True))
def test_packaged_true(*_):
    """Packaged profile selection"""
    expected_name = 'packaged_profile.yaml'
    expected_path = fake_profile_path()
    result_name, result_path = yacfg.files.select_profile_file(expected_name)
    assert result_name == expected_name
    assert result_path == expected_path


@mock.patch('yacfg.files.get_module_path', side_effect=fake_module_path)
@mock.patch('os.path.isfile', side_effect=(True, True, True))
@mock.patch('os.path.abspath', side_effect=fake_os_abspath)
def test_user_true(*_):
    """User Specified profile selection"""
    expected_name = 'user_profile.yaml'
    expected_path = os.path.dirname(fake_os_abspath(''))
    result_name, result_path = yacfg.files.select_profile_file(expected_name)
    assert result_name == expected_name
    assert result_path == expected_path


@mock.patch('yacfg.files.get_module_path', side_effect=fake_module_path)
@mock.patch('os.path.isfile', side_effect=(True, False, True))
@mock.patch('os.path.abspath', side_effect=fake_os_abspath)
def test_user_basedir_true(*_):
    """User Specified profile selection"""
    expected_name = 'user_profile.yaml'
    expected_path = fake_os_abspath(yacfg.meta.PROFILES)
    result_name, result_path = yacfg.files.select_profile_file(expected_name)
    assert result_name == expected_name
    assert result_path == expected_path


@mock.patch('yacfg.files.get_module_path', side_effect=fake_module_path)
@mock.patch('os.path.isfile', side_effect=(True, True, True))
@mock.patch('os.path.abspath', side_effect=fake_os_abspath)
def test_user_both_true(*_):
    """User Specified profile selection"""
    expected_name = 'user_profile.yaml'
    expected_path = os.path.dirname(fake_os_abspath(''))
    result_name, result_path = yacfg.files.select_profile_file(expected_name)
    assert result_name == expected_name
    assert result_path == expected_path


@mock.patch('yacfg.files.get_module_path', side_effect=fake_module_path)
@mock.patch('os.path.isfile', side_effect=(False, False, False))
def test_non_existing(*_):
    """Non-existing packaged profile selection"""
    expected_name = 'non_existing_packaged_profile.yaml'
    with pytest.raises(ProfileError):
        yacfg.files.select_profile_file(expected_name)


@mock.patch('yacfg.files.get_module_path', side_effect=fake_module_path)
@mock.patch('os.path.isfile', side_effect=(False, False, False))
@mock.patch('os.path.abspath', side_effect=fake_os_abspath)
def test_user_non_existing(*_):
    """Non-existing user profile selection"""
    expected_name = 'non_existing_user_profile.yaml'
    with pytest.raises(ProfileError):
        yacfg.files.select_profile_file(expected_name)
