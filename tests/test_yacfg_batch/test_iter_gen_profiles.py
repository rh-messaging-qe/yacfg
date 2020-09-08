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
import yaml
import yacfg_batch
from yacfg_batch.yacfg_batch import iter_gen_profiles
from yacfg_batch.exceptions import YacfgBatchException


@mock.patch('yacfg_batch.yacfg_batch.open', mock.Mock())
@mock.patch('yaml.load_all', mock.Mock())
def test_true(*_):
    filename = 'test.yaml'
    expected_result = [{'a': 1}, {'b': 1}]
    file_desc = mock.sentinel.file_desc
    # noinspection PyUnresolvedReferences
    yacfg_batch.yacfg_batch.open.return_value = file_desc
    yaml.load_all.return_value = expected_result

    result = list(iter_gen_profiles(filename))

    assert expected_result == result

    # noinspection PyUnresolvedReferences
    yacfg_batch.yacfg_batch.open.assert_called()
    # noinspection PyUnresolvedReferences
    yaml.load_all.assert_called_with(file_desc)


@mock.patch('yacfg_batch.yacfg_batch.open',
            side_effect=IOError(
                '[Errno 2] No such file or directory: \'test.yaml\''
            ))
@mock.patch('yaml.load_all', mock.Mock())
def test_io_error(*_):
    filename = 'test.yaml'

    with pytest.raises(YacfgBatchException):
        list(iter_gen_profiles(filename))

    # noinspection PyUnresolvedReferences
    yacfg_batch.yacfg_batch.open.assert_called()
    # noinspection PyUnresolvedReferences
    yaml.load_all.assert_not_called()


@mock.patch('yacfg_batch.yacfg_batch.open', mock.Mock())
@mock.patch('yaml.load_all', side_effect=yaml.YAMLError('Cannot parse'))
def test_yaml_error(*_):
    filename = 'test.yaml'
    file_desc = mock.sentinel.file_desc
    # noinspection PyUnresolvedReferences
    yacfg_batch.yacfg_batch.open.return_value = file_desc

    with pytest.raises(YacfgBatchException):
        list(iter_gen_profiles(filename))

    # noinspection PyUnresolvedReferences
    yacfg_batch.yacfg_batch.open.assert_called()
    # noinspection PyUnresolvedReferences
    yaml.load_all.assert_called()
