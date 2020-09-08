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

from yacfg.files import get_output_filename


def test_jinja_suffix():
    assert get_output_filename('my_config.xml.jinja2') == 'my_config.xml'


def test_base_name():
    assert get_output_filename('my_config.xml') == 'my_config.xml'


dataset_incorrect_values = (
    None,
    1,
    1.0,
    [],
    {},
)


@pytest.mark.parametrize('value', dataset_incorrect_values)
def test_int(value):
    with pytest.raises(TypeError):
        get_output_filename(value)
