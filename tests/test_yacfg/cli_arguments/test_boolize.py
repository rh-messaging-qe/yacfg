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

import yacfg.cli.cli_arguments

dataset_boolize = (
    (None, None),
    ("Yes", True),
    ("No", False),
    ("yes", True),
    ("no", False),
    ("YES", True),
    ("NO", False),
    ("True", True),
    ("False", False),
    ("true", True),
    ("false", False),
    ("TRUE", True),
    ("FALSE", False),
    ("1", True),
    ("0", False),
)


@pytest.mark.parametrize("value,result", dataset_boolize)
def test_boolize_values(value, result):
    assert yacfg.cli.cli_arguments.boolize(value) == result


def test_boolize_exception():
    with pytest.raises(ValueError):
        yacfg.cli.cli_arguments.boolize("test")
