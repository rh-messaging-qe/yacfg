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

import os

import mock
import pytest

import yacfg.output

from yacfg.output import write_output


@mock.patch('yacfg.output.open', mock.MagicMock())
def test_true(*_):
    file_name = 'my_output.txt'
    file_path = '/output/path'
    file_pathname = os.path.join(file_path, file_name)

    data = 'output data'

    write_output(file_name, file_path, data)
    # noinspection PyUnresolvedReferences
    yacfg.output.open.assert_called_with(file_pathname, 'w')
    # noinspection PyUnresolvedReferences
    fh = yacfg.output.open.return_value.__enter__.return_value
    fh.write.assert_has_calls([mock.call(data)])


@mock.patch('yacfg.output.open', side_effect=IOError)
def test_bad_filename(*_):
    file_name = 'my_output.txt'
    file_path = '/bad/output/path'
    file_pathname = os.path.join(file_path, file_name)

    data = 'output data'

    with pytest.raises(IOError):
        write_output(file_name, file_path, data)
    # noinspection PyUnresolvedReferences
    yacfg.output.open.assert_called_with(file_pathname, 'w')
