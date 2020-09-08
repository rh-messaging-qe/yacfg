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
import os.path
import pytest
import mock

from yacfg.files import ensure_output_path


@mock.patch('os.path.isdir', side_effect=(False,))
@mock.patch('os.path.isfile', side_effect=(False,))
def test_create_true(*_):
    output_path = '/location/group/output/'
    with mock.patch('os.makedirs', mock.Mock()):
        ensure_output_path(output_path=output_path)
        # noinspection PyUnresolvedReferences
        os.makedirs.assert_called()


@mock.patch('os.path.isdir', side_effect=(True,))
def test_exists(*_):
    output_path = '/location/group/output/'
    with mock.patch('os.makedirs', mock.Mock()):
        ensure_output_path(output_path=output_path)
        # noinspection PyUnresolvedReferences
        os.makedirs.assert_not_called()


@mock.patch('os.path.isdir', side_effect=(False,))
@mock.patch('os.path.isfile', side_effect=(True,))
def test_exists_but_file_exception(*_):
    output_path = '/location/group/output/'
    with mock.patch('os.makedirs', mock.Mock()):
        with pytest.raises(IOError):
            ensure_output_path(output_path=output_path)
        # noinspection PyUnresolvedReferences
        os.makedirs.assert_not_called()
