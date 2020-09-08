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

import yacfg.files
from yacfg import meta
from yacfg.exceptions import TemplateError
from .fakes import fake_templates_path


@mock.patch('yacfg.files.get_templates_path', side_effect=fake_templates_path)
@mock.patch('os.path.isdir', side_effect=(False, False, True))
@mock.patch('os.path.isfile', side_effect=(True,))
def test_packaged_true(*_):
    """Packaged template selection"""
    template_name = 'product/1.0.0'
    expected_dir = os.path.join(fake_templates_path(), template_name)
    assert yacfg.files.select_template_dir(template_name) == expected_dir


@mock.patch('yacfg.files.get_templates_path', side_effect=fake_templates_path)
@mock.patch('os.path.isdir', side_effect=(False, True, True))
@mock.patch('os.path.isfile', side_effect=(True,))
def test_user_true(*_):
    """User specified template selection"""
    template_name = 'custom/user_product/1.0.0'
    assert yacfg.files.select_template_dir(template_name) == template_name


@mock.patch('yacfg.files.get_templates_path', side_effect=fake_templates_path)
@mock.patch('os.path.isdir', side_effect=(True, False, True))
@mock.patch('os.path.isfile', side_effect=(True,))
def test_user_basedir_true(*_):
    """User specified template selection"""
    template_name = 'user_product/1.0.0'
    expected_name = os.path.join(meta.TEMPLATES, template_name)
    assert yacfg.files.select_template_dir(template_name) == expected_name


@mock.patch('yacfg.files.get_templates_path', side_effect=fake_templates_path)
@mock.patch('os.path.isdir', side_effect=(True, True, True))
@mock.patch('os.path.isfile', side_effect=(True,))
def test_user_both_true(*_):
    """User specified template selection"""
    template_name = 'user_product/1.0.0'
    expected_name = template_name
    assert yacfg.files.select_template_dir(template_name) == expected_name


@mock.patch('yacfg.files.get_templates_path', side_effect=fake_templates_path)
@mock.patch('os.path.isdir', side_effect=(False, False, False))
@mock.patch('os.path.isfile', side_effect=(True,))
def test_not_directory(*_):
    """Template set not a directory"""
    template_name = 'user_product/1.0.0'
    with pytest.raises(TemplateError):
        assert yacfg.files.select_template_dir(template_name) == template_name


@mock.patch('yacfg.files.get_templates_path', side_effect=fake_templates_path)
@mock.patch('os.path.isdir', side_effect=(False, False, True))
@mock.patch('os.path.isfile', side_effect=(False,))
def test_packaged_missing_template_marker(*_):
    """Packaged Template set not a directory"""
    template_name = 'user_product/1.0.0'
    with pytest.raises(TemplateError):
        assert yacfg.files.select_template_dir(template_name) == template_name


@mock.patch('yacfg.files.get_templates_path', side_effect=fake_templates_path)
@mock.patch('os.path.isdir', side_effect=(True, True, True))
@mock.patch('os.path.isfile', side_effect=(False,))
def test_user_missing_template_marker(*_):
    """User specified Template set not a directory"""
    template_name = 'user_product/1.0.0'
    with pytest.raises(TemplateError):
        assert yacfg.files.select_template_dir(template_name) == template_name
