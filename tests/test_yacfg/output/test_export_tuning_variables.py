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

import yacfg.output
from yacfg.exceptions import ProfileError
from yacfg.meta import NAME
from yacfg.output import export_tuning_variables
from ..profiles.fakes import fake_load_profile_defaults, \
    fake_profile_defaults_yaml


@mock.patch('yacfg.output.load_profile_defaults',
            side_effect=fake_load_profile_defaults)
@mock.patch('yacfg.output.ensure_output_path', mock.Mock())
@mock.patch('yacfg.output.write_output', mock.Mock())
def test_true(*_):
    profile_name = 'my_profile.yaml'
    destination_path = '/destination/path/tuning'
    destination_name = 'tuning.yaml'
    destination = os.path.join(destination_path, destination_name)

    expected_data = fake_profile_defaults_yaml()
    expected_data = '# {} tuning file generated from profile {}{}---{}{}'.format(
        NAME, profile_name, os.linesep, os.linesep, expected_data
    )

    export_tuning_variables(profile_name, destination)

    # noinspection PyUnresolvedReferences
    yacfg.output.ensure_output_path.assert_called_with(destination_path)
    # noinspection PyUnresolvedReferences
    yacfg.output.write_output.assert_called_with(destination_name,
                                                 destination_path,
                                                 expected_data)


@mock.patch('yacfg.output.load_profile_defaults',
            side_effect=({},))
@mock.patch('yacfg.output.ensure_output_path', mock.Mock())
@mock.patch('yacfg.output.write_output', mock.Mock())
def test_no_defaults_exception(*_):
    profile_name = 'my_profile.yaml'
    destination_path = '/destination/path/tuning'
    destination_name = 'tuning.yaml'
    destination = os.path.join(destination_path, destination_name)

    with pytest.raises(ProfileError):
        export_tuning_variables(profile_name, destination)

    # noinspection PyUnresolvedReferences
    yacfg.output.ensure_output_path.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.output.write_output.assert_not_called()


@mock.patch('yacfg.output.load_profile_defaults',
            side_effect=fake_load_profile_defaults)
@mock.patch('yacfg.output.ensure_output_path',
            side_effect=OSError('[Errno 13] Permission denied: \'path\''))
@mock.patch('yacfg.output.write_output', mock.Mock())
def test_bad_destination_exception(*_):
    profile_name = 'my_profile.yaml'
    destination_path = '/bad/destination'
    destination_name = 'tuning.yaml'
    destination = os.path.join(destination_path, destination_name)

    with pytest.raises(OSError):
        export_tuning_variables(profile_name, destination)

    # noinspection PyUnresolvedReferences
    yacfg.output.ensure_output_path.assert_called_with(destination_path)
    # noinspection PyUnresolvedReferences
    yacfg.output.write_output.assert_not_called()


@mock.patch('yacfg.output.load_profile_defaults',
            side_effect=fake_load_profile_defaults)
@mock.patch('yacfg.output.ensure_output_path', mock.Mock())
@mock.patch('yacfg.output.write_output',
            side_effect=OSError('[Errno 13] Permission denied: \'path\''))
def test_no_destination_exception(*_):
    profile_name = 'my_profile.yaml'
    destination_path = ''
    destination_name = 'tuning.yaml'
    destination = os.path.join(destination_path, destination_name)

    with pytest.raises(OSError):
        export_tuning_variables(profile_name, destination)

    # noinspection PyUnresolvedReferences
    yacfg.output.ensure_output_path.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.output.write_output.assert_called()
