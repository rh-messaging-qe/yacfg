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

from amqcfg.exceptions import ProfileError
from amqcfg.profiles import load_tuned_profile
from ..profiles.fakes import (
    fake_load_tuned_profile_with_defaults,
    fake_get_tuned_profile,
)


@mock.patch('amqcfg.profiles.get_tuned_profile',
            side_effect=fake_get_tuned_profile)
def test_true(*_):
    profile_name = 'my_profile.yaml'
    expected_data, expected_profile = fake_load_tuned_profile_with_defaults()

    config_data, tuned_profile = load_tuned_profile(profile_name, None)

    assert config_data == expected_data
    assert tuned_profile == expected_profile


@mock.patch('amqcfg.profiles.get_tuned_profile',
            side_effect=('%this is not yaml',))
def test_bad_data_exception(*_):
    profile_name = 'my_profile.yaml'

    with pytest.raises(ProfileError):
        load_tuned_profile(profile_name, None)
