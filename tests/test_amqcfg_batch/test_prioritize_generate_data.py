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

from yacfg_batch.yacfg_batch import (
    prioritize_generate_data,
    GenerateData
)


def test_default(*_):
    default = GenerateData()
    default.profile_name = 'Default Profile'
    default.template_name = 'Default Template'
    default.tuning_files = ['Default Tuning Files']
    default.tuning_data = {'Tuning Data': 'Default', 'Default': 'Tuning data'}

    common = GenerateData()
    profile = GenerateData()

    result = prioritize_generate_data(profile, common, default)
    expected = default

    assert expected == result


def test_default_common(*_):
    default = GenerateData()
    default.profile_name = 'Default Profile'
    default.template_name = 'Default Template'
    default.tuning_files = ['Default Tuning Files']
    default.tuning_data = {'Tuning Data': 'Default', 'Default': 'Tuning data'}

    common = GenerateData()
    common.profile_name = 'Common Profile'
    common.template_name = 'Common Template'
    common.tuning_files = ['Common Tuning Files']
    common.tuning_data = {'Tuning Data': 'Common', 'Common': 'Tuning data'}

    profile = GenerateData()

    expected = GenerateData()
    expected.profile_name = common.profile_name
    expected.template_name = common.template_name
    expected.tuning_files = [] + default.tuning_files + common.tuning_files
    expected.tuning_data = {}
    expected.tuning_data.update(default.tuning_data)
    expected.tuning_data.update(common.tuning_data)

    result = prioritize_generate_data(profile, common, default)

    assert expected == result


def test_default_common_profile(*_):
    default = GenerateData()
    default.profile_name = 'Default Profile'
    default.template_name = 'Default Template'
    default.tuning_files = ['Default Tuning Files']
    default.tuning_data = {'Tuning Data': 'Default', 'Default': 'Tuning data'}

    common = GenerateData()
    common.profile_name = 'Common Profile'
    common.template_name = 'Common Template'
    common.tuning_files = ['Common Tuning Files']
    common.tuning_data = {'Tuning Data': 'Common', 'Common': 'Tuning data'}

    profile = GenerateData()
    profile.profile_name = 'Profile Profile'
    profile.template_name = 'Profile Template'
    profile.tuning_files = ['Profile Tuning Files']
    profile.tuning_data = {'Tuning Data': 'Profile', 'Profile': 'Tuning data'}

    expected = GenerateData()
    expected.profile_name = profile.profile_name
    expected.template_name = profile.template_name
    expected.tuning_files = [] + common.tuning_files + profile.tuning_files
    expected.tuning_data = {}
    expected.tuning_data.update(common.tuning_data)
    expected.tuning_data.update(profile.tuning_data)

    result = prioritize_generate_data(profile, common, default)

    assert expected == result


def test_profile(*_):
    default = GenerateData()

    common = GenerateData()

    profile = GenerateData()
    profile.profile_name = 'Profile Profile'
    profile.template_name = 'Profile Template'
    profile.tuning_files = ['Profile Tuning Files']
    profile.tuning_data = {'Tuning Data': 'Profile', 'Profile': 'Tuning data'}

    expected = profile

    result = prioritize_generate_data(profile, common, default)

    assert expected == result


def test_common(*_):
    default = GenerateData()

    common = GenerateData()
    common.profile_name = 'Common Profile'
    common.template_name = 'Common Template'
    common.tuning_files = ['Common Tuning Files']
    common.tuning_data = {'Tuning Data': 'Common', 'Common': 'Tuning data'}

    profile = GenerateData()

    expected = common

    result = prioritize_generate_data(profile, common, default)

    assert expected == result
