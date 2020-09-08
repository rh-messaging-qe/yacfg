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
    GenerateData
)


def test_str_none(*_):
    generate_data = GenerateData()

    result = str(generate_data)

    expected = 'GenerateData(None, None, None, None)'

    assert expected == result


def test_str_str(*_):
    generate_data = GenerateData()
    generate_data.profile_name = 'a'
    generate_data.template_name = 'b'

    result = str(generate_data)

    expected = "GenerateData('a', 'b', None, None)"

    assert expected == result


def test_eq_empty(*_):
    data1 = GenerateData()
    data2 = GenerateData()

    assert data1 == data2


def test_eq_data(*_):
    data1 = GenerateData()
    data1.profile_name = 'Profile Name'
    data1.template_name = 'Template Name'
    data1.tuning_files = ['Tuning file']
    data1.tuning_data = {'a': 1}

    data2 = GenerateData()
    data2.profile_name = 'Profile Name'
    data2.template_name = 'Template Name'
    data2.tuning_files = ['Tuning file']
    data2.tuning_data = {'a': 1}

    assert data1 == data2


def test_neq_profile_name(*_):
    data1 = GenerateData()
    data1.profile_name = 'Profile Nam'
    data1.template_name = 'Template Name'
    data1.tuning_files = ['Tuning file']
    data1.tuning_data = {'a': 1}

    data2 = GenerateData()
    data2.profile_name = 'Profile Name'
    data2.template_name = 'Template Name'
    data2.tuning_files = ['Tuning file']
    data2.tuning_data = {'a': 1}

    assert data1 != data2


def test_neq_template_name(*_):
    data1 = GenerateData()
    data1.profile_name = 'Profile Name'
    data1.template_name = 'Template Nam'
    data1.tuning_files = ['Tuning file']
    data1.tuning_data = {'a': 1}

    data2 = GenerateData()
    data2.profile_name = 'Profile Name'
    data2.template_name = 'Template Name'
    data2.tuning_files = ['Tuning file']
    data2.tuning_data = {'a': 1}

    assert data1 != data2


def test_neq_tuning_files(*_):
    data1 = GenerateData()
    data1.profile_name = 'Profile Name'
    data1.template_name = 'Template Name'
    data1.tuning_files = ['Tuning fil']
    data1.tuning_data = {'a': 1}

    data2 = GenerateData()
    data2.profile_name = 'Profile Name'
    data2.template_name = 'Template Name'
    data2.tuning_files = ['Tuning file']
    data2.tuning_data = {'a': 1}

    assert data1 != data2


def test_neq_tuning_data(*_):
    data1 = GenerateData()
    data1.profile_name = 'Profile Name'
    data1.template_name = 'Template Name'
    data1.tuning_files = ['Tuning file']
    data1.tuning_data = {'a': 0}

    data2 = GenerateData()
    data2.profile_name = 'Profile Name'
    data2.template_name = 'Template Name'
    data2.tuning_files = ['Tuning file']
    data2.tuning_data = {'a': 1}

    assert data1 != data2
