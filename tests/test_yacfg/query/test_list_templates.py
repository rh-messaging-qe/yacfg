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

from yacfg.query import list_templates
from ..files.fakes import fake_module_path, fake_templates_path


def fake_walk_templates_basic(*_):
    prefix_path = fake_templates_path()
    return [
        (
            os.path.join(prefix_path, 'a'),
            ['modules'],
            ['broker.xml.jinja2', '_template']
        ),
        (
            os.path.join(prefix_path, 'a/modules'),
            ['broker_xml'],
            ['add-on.jinja2']
        ),
        (
            os.path.join(prefix_path, 'a/modules/broker_xml'),
            [],
            ['queues.jinja2']
        ),
        (
            os.path.join(prefix_path, 'b'),
            ['1.0.0'], []
        ),
        (
            os.path.join(prefix_path, 'b/1.0.0'),
            ['modules'],
            ['management.xml.jinja2', 'artemis-roles.properties.jinja2',
             'broker.xml.jinja2', 'artemis.profile.jinja2',
             'bootstrap.xml.jinja2', 'jolokia-access.xml.jinja2',
             'artemis-users.properties.jinja2',
             'logging.properties.jinja2',
             'login.config.jinja2', '_template']
        ),
        (
            os.path.join(prefix_path, 'b/1.0.0/modules'),
            [], ['broker_xml.jinja2']
        ),
        (
            os.path.join(prefix_path, 'not_a_template'),
            ['a'],
            ['acceptors.jinja2', 'store.jinja2',
             'cluster_connections.jinja2',
             'security_settings.jinja2', 'journal.jinja2',
             'broadcast_group.jinja2', 'discovery_group.jinja2',
             'cluster.jinja2', 'addresses.jinja2',
             'critical_analyzer.jinja2',
             'grouping_handler.jinja2', 'ha_policy.jinja2',
             'duplicate_cache.jinja2', 'queue.jinja2',
             'broker_plugins.jinja2',
             'wildcards_addresses.jinja2', 'address_settings.jinja2',
             'connectors.jinja2']),
        (
            os.path.join(prefix_path, 'not_a_template/a'),
            ['x'],
            ['security_setting.jinja2', 'security_setting_plugin.jinja2']
        ),
        (
            os.path.join(prefix_path, 'not_a_template/a/x'),
            [],
            ['jdbc.jinja2']
        ),
    ]


@mock.patch('yacfg.query.get_module_path', side_effect=fake_module_path)
@mock.patch('os.walk', side_effect=fake_walk_templates_basic)
def test_true(*_):
    expected = [
        'a',
        'b/1.0.0',
    ]

    result = list_templates()
    assert expected == result


def fake_walk_templates_not_a_template(*_):
    prefix_path = fake_templates_path()
    return [
        (
            os.path.join(prefix_path, 'not_a_template'),
            ['a'],
            ['acceptors.jinja2', 'store.jinja2',
             'cluster_connections.jinja2',
             'security_settings.jinja2', 'journal.jinja2',
             'broadcast_group.jinja2', 'discovery_group.jinja2',
             'cluster.jinja2', 'addresses.jinja2',
             'critical_analyzer.jinja2',
             'grouping_handler.jinja2', 'ha_policy.jinja2',
             'duplicate_cache.jinja2', 'queue.jinja2',
             'broker_plugins.jinja2',
             'wildcards_addresses.jinja2', 'address_settings.jinja2',
             'connectors.jinja2']),
        (
            os.path.join(prefix_path, 'not_a_template/a'),
            ['x'],
            ['security_setting.jinja2', 'security_setting_plugin.jinja2']
        ),
        (
            os.path.join(prefix_path, 'not_a_template/a/x'),
            [],
            ['jdbc.jinja2']
        ),
    ]


@mock.patch('yacfg.query.get_module_path', side_effect=fake_module_path)
@mock.patch('os.walk', side_effect=fake_walk_templates_not_a_template)
def test_not_a_template(*_):
    expected = []

    result = list_templates()
    assert expected == result


@mock.patch('yacfg.query.get_module_path', side_effect=fake_module_path)
@mock.patch('os.walk', side_effect=((),))
def test_empty(*_):
    expected = []

    result = list_templates()
    assert expected == result
