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

from __future__ import annotations

import os


def fake_module_path() -> str:
    return "/module/path"


def fake_profiles_paths() -> list[str]:
    return [os.path.join(fake_module_path(), 'profiles')]


def fake_templates_paths() -> list[str]:
    return [os.path.join(fake_module_path(), 'templates')]


def fake_os_abspath(path):
    return os.path.join("/absolute/path/", path)


def fake_select_profile_file(name: str) -> tuple[str, str]:
    return name, fake_profiles_paths()[0]


def fake_select_template_dir(name: str) -> str:
    return os.path.join(fake_templates_paths()[0], name)
