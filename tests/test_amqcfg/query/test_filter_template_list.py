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

from yacfg.query import filter_template_list

basic_template_list = [
    'a.xml',
    'a.txt',
    'b.xml',
    'b.txt',
    'c.xml',
    'c.properties',
]

dataset_filter_basic = (
    ([''], basic_template_list),
    (['a.*'], ['a.xml', 'a.txt']),
    (['b.*'], ['b.xml', 'b.txt']),
    (['.*xml'], ['a.xml', 'b.xml', 'c.xml']),
    (['.*xml', '.*txt'], ['a.xml', 'a.txt', 'b.xml', 'b.txt', 'c.xml']),
    (['xxx'], []),
)


@pytest.mark.parametrize('output_filter,expected_result', dataset_filter_basic)
def test_filter_basic(output_filter, expected_result):
    result = filter_template_list(basic_template_list,
                                  output_filter=output_filter)
    assert result == expected_result
