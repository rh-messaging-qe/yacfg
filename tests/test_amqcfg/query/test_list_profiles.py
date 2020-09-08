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

from yacfg.query import list_profiles
from ..files.fakes import fake_profile_path, fake_module_path


def fake_os_walk_profiles_basic(*_):
    prefix_path = fake_profile_path()
    return [
        (
            os.path.join(prefix_path, ''),
            ['a', 'b', 'x', '_not'],
            ['profile.yaml']
        ),
        (
            os.path.join(prefix_path, 'a'),
            ['b'],
            ['profile.yaml', 'something.txt']
        ),
        (
            os.path.join(prefix_path, 'a', 'b'),
            [],
            ['profile.yaml']
        ),
        (
            os.path.join(prefix_path, 'b'),
            [],
            ['my_profile.yaml']
        ),
        (
            os.path.join(prefix_path, 'x'),
            ['_not'],
            ['something.txt']
        ),
        (
            os.path.join(prefix_path, 'x', '_not'),
            [],
            ['not_a_profile.yaml']
        ),
        (
            os.path.join(prefix_path, '_not'),
            [],
            ['also_not_a_profile.yaml']
        ),
    ]


@mock.patch('yacfg.query.get_module_path',
            side_effect=fake_module_path)
@mock.patch('os.walk', side_effect=fake_os_walk_profiles_basic)
def test_basic(*_):
    expected = [
        'profile.yaml',
        'a/profile.yaml',
        'a/b/profile.yaml',
        'b/my_profile.yaml',
    ]
    result = list_profiles()
    assert expected == result


def fake_os_walk_not_a_profile(*_):
    prefix_path = fake_profile_path()
    return [
        (
            os.path.join(prefix_path, 'x'),
            ['_not'],
            ['something.txt']
        ),
        (
            os.path.join(prefix_path, 'x', '_not'),
            [],
            ['not_a_profile.yaml']
        ),
        (
            os.path.join(prefix_path, '_not'),
            [],
            ['also_not_a_profile.yaml']
        ),
    ]


@mock.patch('yacfg.query.get_module_path',
            side_effect=fake_module_path)
@mock.patch('os.walk', side_effect=fake_os_walk_not_a_profile)
def test_not_a_profile(*_):
    expected = []
    result = list_profiles()
    assert expected == result


@mock.patch('yacfg.query.get_module_path',
            side_effect=fake_module_path)
@mock.patch('os.walk', side_effect=((),))
def test_empty(*_):
    expected = []
    result = list_profiles()
    assert expected == result
