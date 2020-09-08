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
    extract_generate_data,
    GenerateData
)


def test_empty(*_):
    profile_file_data = {}

    result = extract_generate_data(profile_file_data)

    expected = GenerateData()

    assert expected == result


def test_default(*_):
    profile_file_data = {
        '_default': {
            'profile': 'Profile Name'
        }
    }

    result = extract_generate_data(profile_file_data)

    expected = GenerateData()
    expected.profile_name = 'Profile Name'

    assert expected == result


def test_section(*_):
    profile_file_data = {
        '_section': {
            'profile': 'Profile Name'
        }
    }

    result = extract_generate_data(profile_file_data, '_section')

    expected = GenerateData()
    expected.profile_name = 'Profile Name'

    assert expected == result


def test_data(*_):
    profile_file_data = {
        '_default': {
            'profile': 'Profile Name',
            'template': 'Template Name',
            'tuning_files': ['Tuning Files'],
            'tuning': {
                'a': 1,
            }
        }
    }

    result = extract_generate_data(profile_file_data)

    expected = GenerateData()
    expected.profile_name = 'Profile Name'
    expected.template_name = 'Template Name'
    expected.tuning_files = ['Tuning Files']
    expected.tuning_data = {'a': 1}

    assert expected == result
