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

import yacfg_batch
from yacfg_batch.yacfg_batch import generate
from .fakes import (
    fake_iter_gen_profiles_one,
    fake_iter_gen_profiles_two,
    fake_common_one,
    fake_default_one,
    fake_common_two,
    fake_default_two,
)


@mock.patch('yacfg_batch.yacfg_batch.generate_all_profiles', mock.Mock())
@mock.patch('yacfg_batch.yacfg_batch.iter_gen_profiles',
            fake_iter_gen_profiles_one)
def test_one(*_):
    input_files = ['a/b.yaml']
    generate(input_files)

    # noinspection PyUnresolvedReferences
    yacfg_batch.yacfg_batch.generate_all_profiles.assert_called_with(
        'a',
        None,
        fake_default_one,
        fake_common_one,
        next(fake_iter_gen_profiles_one(None))
    )


@mock.patch('yacfg_batch.yacfg_batch.generate_all_profiles', mock.Mock())
@mock.patch('yacfg_batch.yacfg_batch.iter_gen_profiles',
            fake_iter_gen_profiles_two)
def test_two(*_):
    input_files = ['a/b.yaml']
    generate(input_files)

    profile_data = list(fake_iter_gen_profiles_two(None))

    calls = [
        mock.call('a', None, fake_default_one,
                  fake_common_one, profile_data[0]),
        mock.call('a', None, fake_default_two,
                  fake_common_two, profile_data[1]),
    ]

    # noinspection PyUnresolvedReferences
    yacfg_batch.yacfg_batch.generate_all_profiles.assert_has_calls(
        calls
    )


@mock.patch('yacfg_batch.yacfg_batch.generate_all_profiles', mock.Mock())
@mock.patch('yacfg_batch.yacfg_batch.iter_gen_profiles',
            fake_iter_gen_profiles_two)
def test_two_files_two(*_):
    input_files = ['a/b.yaml', 'c/d.yaml']
    generate(input_files)

    profile_data = list(fake_iter_gen_profiles_two(None))

    calls = [
        mock.call('a', None, fake_default_one,
                  fake_common_one, profile_data[0]),
        mock.call('a', None, fake_default_two,
                  fake_common_two, profile_data[1]),
        mock.call('c', None, fake_default_one,
                  fake_common_one, profile_data[0]),
        mock.call('c', None, fake_default_two,
                  fake_common_two, profile_data[1]),
    ]

    # noinspection PyUnresolvedReferences
    yacfg_batch.yacfg_batch.generate_all_profiles.assert_has_calls(
        calls
    )
