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

import yacfg
from yacfg_batch.yacfg_batch import generate_all_profiles, GenerateData
from yacfg_batch.exceptions import YacfgBatchException


@mock.patch('yacfg.yacfg.generate', mock.Mock())
def test_no_profile_name(*_):
    input_path = ''
    output_path = ''
    default = GenerateData()
    common = GenerateData()
    profile_file_data = {
        'service': {'pass': True}
    }

    with pytest.raises(YacfgBatchException):
        generate_all_profiles(
            input_path,
            output_path,
            default,
            common,
            profile_file_data
        )


@mock.patch('yacfg.yacfg.generate', mock.Mock())
def test_basic(*_):
    input_path = ''
    output_path = ''
    default = GenerateData()
    common = GenerateData()
    profile_file_data = {
        'service': {
            'profile': 'test',
        }
    }

    generate_all_profiles(
        input_path,
        output_path,
        default,
        common,
        profile_file_data
    )

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.generate.assert_called_with(
        profile='test',
        template=None,
        output_path=None,
        tuning_files_list=None,
        tuning_data_list=None,
    )


@mock.patch('yacfg.yacfg.generate', mock.Mock())
def test_advanced(*_):
    input_path = ''
    output_path = 'test'
    default = GenerateData()
    default.profile_name = 'test2'
    common = GenerateData()
    profile_file_data = {
        '_default': {
            'profile': 'test2',
        },
        'service': {
            'profile': 'test',
        },
        'service2': {
            'tuning_files': ['a']
        },
        'service3': {
            'template': 'My Template',
            'tuning': {
                'a': 1
            }
        }
    }

    generate_all_profiles(
        input_path,
        output_path,
        default,
        common,
        profile_file_data
    )
    import os

    calls = [
        mock.call(profile='test', template=None, output_path=os.path.join('test','service'),
                  tuning_files_list=None, tuning_data_list=None),
        mock.call(profile='test2', template=None, output_path=os.path.join('test','service2'),
                  tuning_files_list=['a'], tuning_data_list=None),
        mock.call(profile='test2', template='My Template',
                  output_path=os.path.join('test','service3'), tuning_files_list=None,
                  tuning_data_list=[{'a': 1}]),
    ]

    # noinspection PyUnresolvedReferences
    yacfg.yacfg.generate.assert_has_calls(calls, any_order=True)
