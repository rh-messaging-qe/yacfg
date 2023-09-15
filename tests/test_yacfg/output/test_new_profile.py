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
import shutil

import mock
import pytest

import yacfg.output
from yacfg.output import new_profile
from ..files.fakes import fake_select_profile_file, fake_profiles_paths


@mock.patch("yacfg.files.select_profile_file", side_effect=fake_select_profile_file)
@mock.patch("shutil.copyfile", mock.Mock())
@mock.patch("yacfg.files.ensure_output_path", mock.Mock())
def test_true(*_):
    """Creating new profile true path"""
    profile_name = "existing_profile.yaml"
    destination = "/output/directory/my_new_profile.yaml"
    expected_source_file = os.path.join(fake_profiles_paths()[0], profile_name)
    expected_target_file = destination
    expected_target_dir = os.path.dirname(destination)

    new_profile(profile_name, destination)
    # noinspection PyUnresolvedReferences
    yacfg.files.ensure_output_path.assert_called_with(expected_target_dir)
    # noinspection PyUnresolvedReferences
    shutil.copyfile.assert_called_with(expected_source_file, expected_target_file)


@mock.patch("yacfg.files.select_profile_file", side_effect=fake_select_profile_file)
@mock.patch("shutil.copyfile", mock.Mock())
@mock.patch("yacfg.files.ensure_output_path", mock.Mock())
def test_true_no_destination(*_):
    """Creating new profile true path"""
    profile_name = "existing_profile.yaml"
    destination = "my_new_profile.yaml"
    expected_source_file = os.path.join(fake_profiles_paths()[0], profile_name)
    expected_target_file = destination

    new_profile(profile_name, destination)
    # noinspection PyUnresolvedReferences
    yacfg.files.ensure_output_path.assert_not_called()
    # noinspection PyUnresolvedReferences
    shutil.copyfile.assert_called_with(expected_source_file, expected_target_file)


@mock.patch("yacfg.files.select_profile_file", side_effect=fake_select_profile_file)
@mock.patch("shutil.copyfile", mock.Mock())
@mock.patch(
    "yacfg.files.ensure_output_path",
    side_effect=OSError("[Errno 13] Permission denied: 'path'"),
)
def test_destination_problem_exception(*_):
    """Creating new profile true path"""
    profile_name = "existing_profile.yaml"
    destination = "/problematic/directory/my_new_profile.yaml"
    expected_target_dir = os.path.dirname(destination)

    with pytest.raises(OSError):
        new_profile(profile_name, destination)
    # noinspection PyUnresolvedReferences
    yacfg.files.ensure_output_path.assert_called_with(expected_target_dir)
    # noinspection PyUnresolvedReferences
    shutil.copyfile.assert_not_called()
