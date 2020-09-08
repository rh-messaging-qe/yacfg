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
from yacfg.profiles import load_profile_defaults
from .fakes import (
    fake_load_profile_defaults,
    fake_get_tuned_profile,
)


@mock.patch('yacfg.profiles.get_profile_template', mock.Mock())
def test_true(*_):
    profile_name = 'profile.yaml'
    expected_data = fake_load_profile_defaults()

    # fake jinja template
    fake_template = mock.Mock()
    yacfg.profiles.get_profile_template.return_value = fake_template
    fake_template.render.return_value = fake_get_tuned_profile()

    profile_defaults = load_profile_defaults(profile_name)

    assert profile_defaults == expected_data
    # noinspection PyUnresolvedReferences
    yacfg.profiles.get_profile_template.assert_called_with(profile_name)


@mock.patch('yacfg.profiles.get_profile_template',
            side_effect=TemplateError)
def test_bad_template(*_):
    profile_name = 'bad_profile.yaml'

    with pytest.raises(TemplateError):
        load_profile_defaults(profile_name)
