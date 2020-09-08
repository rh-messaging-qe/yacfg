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

from yacfg_batch.yacfg_batch import GenerateData


def fake_iter_gen_profiles_one(filename):
    del filename
    yield {
        '_default': {
            'tuning_files': ['a', 'b']
        },
        '_common': {
            'profile': 'Profile Name'
        }
    }


def fake_iter_gen_profiles_two(filename):
    del filename
    yield {
        '_default': {
            'tuning_files': ['a', 'b']
        },
        '_common': {
            'profile': 'Profile Name'
        }
    }
    yield {
        '_default': {
            'tuning_files': ['c', 'd']
        },
        '_common': {
            'profile': 'Profile Name 2'
        }
    }


fake_default_one = GenerateData()
fake_default_one.tuning_files = ['a', 'b']

fake_common_one = GenerateData()
fake_common_one.profile_name = 'Profile Name'

fake_default_two = GenerateData()
fake_default_two.tuning_files = ['c', 'd']

fake_common_two = GenerateData()
fake_common_two.profile_name = 'Profile Name 2'
