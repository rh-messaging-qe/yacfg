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

import yacfg.files
from .fakes import fake_module_path, fake_profile_path, \
    fake_templates_path


@mock.patch('yacfg.files.get_module_path', side_effect=fake_module_path)
def test_get_profiles_path(_):
    expected = fake_profile_path()
    assert yacfg.files.get_profiles_path() == expected


@mock.patch('yacfg.files.get_module_path', side_effect=fake_module_path)
def test_get_templates_path(_):
    expected = fake_templates_path()
    assert yacfg.files.get_templates_path() == expected
