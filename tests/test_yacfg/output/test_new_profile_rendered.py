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

import mock as mock
import pytest

import yacfg.output
from yacfg.output import new_profile_rendered
from yacfg.meta import NAME
from ..profiles.fakes import (
    fake_load_tuned_profile_with_defaults,
    fake_load_tuned_profile_no_defaults,
)


@mock.patch('yacfg.output.get_tuned_profile',
            side_effect=fake_load_tuned_profile_with_defaults)
@mock.patch('yacfg.output.write_output', mock.Mock())
@mock.patch('yacfg.output.ensure_output_path', mock.Mock())
def test_true_defaults(*_):
    profile_name = 'product/1.0.0/my_profile.yaml'
    destination_name = 'destination_profile.yaml'
    destination_path = '/profile/destination/path'
    destination = os.path.join(destination_path, destination_name)
    _, expected_data = fake_load_tuned_profile_no_defaults()
    expected_data = '# {} tuning file generated from profile {}{}---{}{}'.format(
        NAME, profile_name, os.linesep, os.linesep, expected_data
    )

    new_profile_rendered(profile_name, destination, None)
    # noinspection PyUnresolvedReferences
    yacfg.output.ensure_output_path.assert_called_with(destination_path)
    # noinspection PyUnresolvedReferences
    yacfg.output.write_output.assert_called_with(destination_name,
                                                 destination_path,
                                                 expected_data)


@mock.patch('yacfg.output.get_tuned_profile',
            side_effect=fake_load_tuned_profile_no_defaults)
@mock.patch('yacfg.output.write_output', mock.Mock())
@mock.patch('yacfg.output.ensure_output_path', mock.Mock())
def test_true_no_defaults(*_):
    profile_name = 'product/1.0.0/my_profile.yaml'
    destination_name = 'destination_profile.yaml'
    destination_path = '/profile/destination/path'
    destination = os.path.join(destination_path, destination_name)
    _, expected_data = fake_load_tuned_profile_no_defaults()
    expected_data = '# {} tuning file generated from profile {}{}---{}{}'.format(
        NAME, profile_name, os.linesep, os.linesep, expected_data
    )

    new_profile_rendered(profile_name, destination, None)
    # noinspection PyUnresolvedReferences
    yacfg.output.ensure_output_path.assert_called_with(destination_path)
    # noinspection PyUnresolvedReferences
    yacfg.output.write_output.assert_called_with(destination_name,
                                                 destination_path,
                                                 expected_data)


@mock.patch('yacfg.output.get_tuned_profile',
            side_effect=fake_load_tuned_profile_with_defaults)
@mock.patch('yacfg.output.write_output', mock.Mock())
@mock.patch('yacfg.output.ensure_output_path', mock.Mock())
def test_true_no_destination(*_):
    profile_name = 'product/1.0.0/my_profile.yaml'
    destination = ''
    _, expected_data = fake_load_tuned_profile_no_defaults()
    expected_data = '# {} tuning file generated from profile {}{}---{}{}'.format(
        NAME, profile_name, os.linesep, os.linesep, expected_data
    )

    new_profile_rendered(profile_name, destination, None)
    # noinspection PyUnresolvedReferences
    yacfg.output.ensure_output_path.assert_not_called()
    # noinspection PyUnresolvedReferences
    yacfg.output.write_output.assert_called_with(destination,
                                                 destination,
                                                 expected_data)


@mock.patch('yacfg.output.get_tuned_profile',
            side_effect=fake_load_tuned_profile_with_defaults)
@mock.patch('yacfg.output.ensure_output_path',
            side_effect=OSError('[Errno 13] Permission denied: \'path\''))
@mock.patch('yacfg.output.write_output', mock.Mock())
def test_destination_problem_exception(*_):
    profile_name = 'product/1.0.0/my_profile.yaml'
    destination = '/problematic/destination'
    with pytest.raises(OSError):
        new_profile_rendered(profile_name, destination, None)
    # noinspection PyUnresolvedReferences
    yacfg.output.ensure_output_path.assert_called()
    # noinspection PyUnresolvedReferences
    yacfg.output.write_output.assert_not_called()
