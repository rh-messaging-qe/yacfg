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

import logging
import os
import shutil

import yaml

from .exceptions import ProfileError
from .files import select_profile_file, ensure_output_path, select_template_dir
from .meta import NAME
from .profiles import load_profile_defaults, get_tuned_profile

LOG = logging.getLogger(__name__)


# pyyaml workaround
# https://stackoverflow.com/questions/25108581/python-yaml-dump-bad-indentation
# https://github.com/yaml/pyyaml/issues/234
class MyDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def yaml_dump_wrapper(data):
    """YAML dump unified call wrapper

    :param data: data passed to yaml.dump
    :type data: dict
    :return: dumped yaml
    :rtype: str
    """
    return yaml.dump(
        data=data,
        Dumper=MyDumper,
        default_flow_style=False,
        explicit_start=True,
        explicit_end=False,
        width=140,
    )


def new_profile(profile, dest_profile):
    """Export an existing profile

    :param profile: existing profile name (from user or packaged)
    :type profile: str
    :param dest_profile: filename of new profile
    :type dest_profile: str

    :raises OSError: if there is a problem with destination path
    :raises ProfileError: if there is a problem with the existing template
    """
    profile_name, profile_path = select_profile_file(profile)
    src = os.path.join(profile_path, profile_name)

    dest_path = os.path.dirname(dest_profile)
    if dest_path:
        ensure_output_path(dest_path)  # raises: OSError

    shutil.copyfile(src, dest_profile)


def new_profile_rendered(profile, dest_profile, tuning_files=None,
                         tuning_data_list=None):
    """Export an existing profile in static form, stripped defaults section

    :param profile: existing profile name (from user or packaged)
    :type profile: str
    :param dest_profile: filename of new profile
    :type dest_profile: str
    :param tuning_files: user specified tuning file path
    :type tuning_files: list[str] | None
    :param tuning_data_list: user specific tuning data list
        provided directly
    :type tuning_data_list: list[dict] | None

    :raises OSError: if there is a problem with destination path
    :raises ProfileError: if there is a problem with the existing template
    """
    config_data, _ = get_tuned_profile(profile, tuning_files, tuning_data_list)

    dest_path = os.path.dirname(dest_profile)
    dest_name = os.path.basename(dest_profile)
    if dest_path:
        ensure_output_path(dest_path)  # raises: OSError

    if '_defaults' in config_data:
        del config_data['_defaults']

    export_data = yaml_dump_wrapper(config_data)

    export_data = '# {} tuning file generated from profile {}{}{}'.format(
        NAME, profile, os.linesep, export_data
    )
    write_output(dest_name, dest_path, export_data)


def new_template(template, dest_template):
    """Export an existing template dir

    :param template: existing template name (from user or packaged)
    :type template: str
    :param dest_template: dirname of new profile
    :type dest_template: str

    :raises OSError: if there is problem with destination path
    :raises TemplateError: if there is a problem with existing template
    """
    template_path = select_template_dir(template)

    shutil.copytree(template_path, dest_template, symlinks=False)


def export_tuning_variables(profile_name, dest_file):
    """Export subsection of profile tunable variables to new yaml file

    :param profile_name: profile name (user defined or packaged)
    :type profile_name: str
    :param dest_file: filename of destination tuning file
    :type dest_file: str

    :raises OSError: if there is s problem with destination path
    :raises ProfileError: if there is a problem with selected profile
    """

    defaults_data = load_profile_defaults(profile_name)
    if not defaults_data:
        raise ProfileError(
            'Selected profile "%s" does not contain any tunable variables'
            % profile_name
        )

    dest_path = os.path.dirname(dest_file)
    dest_name = os.path.basename(dest_file)
    if dest_path:
        ensure_output_path(dest_path)  # raises: OSError

    # export_data = yaml.dump_all([defaults_data], default_flow_style=False)
    export_data = yaml_dump_wrapper(defaults_data)

    LOG.debug('Exported tuning data:\n%s', export_data)
    export_data = '# {} tuning file generated from profile {}{}{}'.format(
        NAME, profile_name, os.linesep, export_data
    )
    write_output(dest_name, dest_path, export_data)
    LOG.info('Tuning data exported')


def write_output(filename, output_path, data):
    """Helper to write generated data to file

    :param filename: name of output file
    :type filename: str
    :param output_path: main path for generating files
    :type output_path: str
    :param data: data to write
    :type data: str
    """
    filepath = os.path.join(output_path, filename)
    with open(filepath, 'w') as fh:
        fh.write(data)
        # fh.write(os.linesep)
    LOG.debug('File writen "%s"', filepath)
