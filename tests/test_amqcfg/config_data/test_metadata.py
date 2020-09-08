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

import pytest

import yacfg.config_data

dataset_metadata_members = (
    'tool_name',
    'datetime',
)


@pytest.mark.parametrize('member', dataset_metadata_members)
def test_add_template_metadata_check_member(member):
    data = {}
    yacfg.config_data.add_template_metadata(data)
    assert member in data['metadata']


dataset_metadata_datetime_members = (
    'datetime',
    'year',
    'time',
    'date',
    'unix',
)


@pytest.mark.parametrize('member', dataset_metadata_datetime_members)
def test_add_template_metadata_datetime_check_member(member):
    data = {}
    yacfg.config_data.add_template_metadata(data)
    assert member in data['metadata']['datetime']
