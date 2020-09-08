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


def fake_get_tuned_profile_data(*_):
    return {'_defaults': {'default_key': 'default_value'}, 'key': 'value'}


def fake_get_tuned_profile(*_):
    return (
        '_defaults:\n'
        '  default_key: default_value\n'
        ''
        'key: value\n'
    )


def fake_load_tuned_profile_with_defaults(*_):
    return (
        fake_get_tuned_profile_data(),
        fake_get_tuned_profile()
    )


def fake_load_tuned_profile_no_defaults(*_, **kwargs):
    del kwargs
    return (
        {'key': 'value'},
        (
            'key: value\n'
        )
    )


def fake_load_tuned_profile_w_template(*_, **kwargs):
    del kwargs
    return (
        {'render': {'template': 'template/1.0.0'}, 'key': 'value'},
        (
            '_render:\n'
            '  template: template/1.0.0\n'
            '\n'
            'key: value\n'
        )
    )


def fake_load_profile_defaults(*_):
    return {'default_key': 'default_value'}


def fake_profile_defaults_yaml(*_):
    return (
        'default_key: default_value\n'
    )
