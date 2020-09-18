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
import itertools
import logging
import os

import yaml
from jinja2 import Environment, FileSystemLoader

from .exceptions import ProfileError, TemplateError
from .files import select_profile_file, get_profiles_path

LOG = logging.getLogger(__name__)


def load_tuning_files(tuning_files=None):
    """Load tuning data from requested tuning files in order and
    provides list of tuning data for further processing.

    :param tuning_files: list of tuning files names
    :type tuning_files: list[str] | None

    :return: list of tuning data loaded from yaml tuning files
    :rtype: list[dict]
    """

    tuning_values_list = []

    if tuning_files:
        for tuning_file in tuning_files:
            try:
                tuning_values_list.append(yaml.load(stream=open(tuning_file, 'r'), Loader=yaml.SafeLoader))
            except IOError as exc:
                raise ProfileError(
                    'Unable to open tuning file "{}" {}'.format(
                        tuning_file, exc
                    )
                )
            except yaml.YAMLError as exc:
                raise ProfileError(
                    'Unable to parse YAML tuning file "{}" {}'.format(
                        tuning_files, exc
                    )
                )
            LOG.debug('Tuning file {} loaded', tuning_file)
    else:
        LOG.debug('No tuning files requested.')

    return tuning_values_list


def load_tuning(profile_defaults=None, tuning_files_list=None,
                tuning_data_list=None):
    """Load and apply all tuning, from profile defaults, from tuning
    files, and then directly provided tuning data. If provided.
    All data is applied in order.

    :param profile_defaults: profile defaults data to be tuned
    :type profile_defaults: dict | None
    :param tuning_files_list: list of tuning files names
    :type tuning_files_list: list[str] | None
    :param tuning_data_list: list of tuning data directly provided
    :type tuning_data_list: list[dict] | None

    :return: compound overlaid tuning data in order of appearance
    :rtype: dict
    """
    result = {}
    files_tuning_values = load_tuning_files(tuning_files_list)
    if profile_defaults:
        result.update(profile_defaults)
    if tuning_data_list is None:
        tuning_data_list = []

    for tuning_data in itertools.chain(files_tuning_values, tuning_data_list):
        result.update(tuning_data)

    return result


def get_tuned_profile(profile, tuning_files_list=None, tuning_data_list=None):
    """Get selected profile and use tuning data to fine tune
     it's variable values.

    :param profile: profile name (packaged) or path to profile
        (user specified)
    :type profile: str
    :param tuning_files_list: list of files with tuning data to be used
    :type tuning_files_list: list[str] | None
    :param tuning_data_list: data used to tune the variable values.
    :type tuning_data_list: list[dict] | None

    :raises ProfileError: when tuned profile is not valid.

    :return: compound tuned config data, and tuned profile yaml
    :rtype: dict, str
    """
    tuning_data = load_tuning(
        profile_defaults=load_profile_defaults(profile),
        tuning_files_list=tuning_files_list,
        tuning_data_list=tuning_data_list,
    )

    tuning_profile = get_profile_template(profile)
    tuning_data['profile_path'] = tuning_profile.name
    tuned_profile = tuning_profile.render(tuning_data)

    try:
        config_data = yaml.load(stream=tuned_profile, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        raise ProfileError(
            'Unable to parse tuned profile "{}" {}'.format(
                profile, exc
            )
        )

    return config_data, tuned_profile


def load_profile_defaults(profile):
    """Load defaults variables from a profile if available

    .. note: profile will be rendered as scratch without any values
        to be able to be loaded as valid yaml.

    :param profile: profile name (from package or from user)
    :type profile: str

    :return: defaults values mapping, if not available then empty dict
    :rtype: dict
    """
    # scratch render of profile template for _defaults extraction
    scratch_profile = get_profile_template(profile)
    scratch_profile = scratch_profile.render()
    tmp_data = yaml.load(stream=scratch_profile, Loader=yaml.SafeLoader)
    tuning_data = tmp_data.get('_defaults', {})
    LOG.debug('Tuning data: %s', tuning_data)
    return tuning_data


def get_profile_template(profile_name):
    """Get a jinja2 template via env generated for selected profile
    (for fine-tuning of profile)

    :param profile_name: name of template set
        (alternatively path to user specified template set)
    :type profile_name: str

    :return: jinja2 profile template for fine tuning template
    :rtype: Template
    """

    selected_template_name, selected_template_path = \
        select_profile_file(profile_name)

    if not os.path.isdir(selected_template_path):
        raise TemplateError(
            'Unable to load requested profile location "%s"' % profile_name
        )

    env = Environment(
        loader=FileSystemLoader([
            selected_template_path,  # selected template
            get_profiles_path(),
        ]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template(selected_template_name)

    return template
