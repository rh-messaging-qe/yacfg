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

import yaml
from jinja2 import Environment, FileSystemLoader

from .exceptions import ProfileError, TemplateError
from .files import select_profile_file, get_profiles_path

LOG = logging.getLogger(__name__)


def load_tuned_profile(profile, tuning_files):
    """Load a complete tuned profile, get config_data as well
    as rendered profile

    :param profile: profile name (packaged or user specified)
    :type profile: str
    :param tuning_files: tuning file to tune variables
    :type tuning_files: list[str] or None

    :raises ProfileError: if there is problem with loading the profile data
    :raises ProfileError: when there is problem opening tuning file
    :raises ProfileError: when there is problem with tuning file parsing
    :raises ProfileError: when there is problem with loading profile

    :return: config_data and rendered tuned profile
    :rtype: tuple[dict, str]
    """
    # fine tuning profile
    tuned_profile = get_tuned_profile(profile, tuning_files)
    # loading tuned profile data
    try:
        config_data = yaml.load(tuned_profile)
    except yaml.YAMLError as exc:
        raise ProfileError(
            'Unable to parse YAML profile "%s" tuned by "%s" %s'
            % (profile, tuning_files, exc))
    return config_data, tuned_profile


def get_tuned_profile(profile, tuning_files):
    """Get selected profile and use tuning file to fine tune
    it's variable values.

    :param profile: profile name (packaged) or path to profile file (user)
    :type profile: str
    :param tuning_files: path to user specified tuning file (yaml)
    :type tuning_files: list[str] or None

    :raises ProfileError: when there is problem opening tuning file
    :raises ProfileError: when there is problem with tuning file parsing
    :raises ProfileError: when there is problem with loading profile

    :return: fine tuned profile yaml to be loaded for templating
    :rtype: str
    """
    tuning_data = load_profile_defaults(profile)

    if tuning_files:
        for tuning_file in tuning_files:
            try:
                tuning_values = yaml.load(open(tuning_file, 'r'))
            except IOError as exc:
                raise ProfileError(
                    'Unable to open tuning file "%s" %s' % (tuning_file, exc)
                )
            except yaml.YAMLError as exc:
                raise ProfileError(
                    'Unable to parse YAML tuning file "%s" %s'
                    % (tuning_files, exc)
                )
            tuning_data.update(tuning_values)
            LOG.debug('Profile "%s" tuned with "%s"', profile, tuning_file)
    else:
        LOG.debug('Profile "%s" using _defaults', profile)

    tuning_profile = get_profile_template(profile)
    tuned_profile = tuning_profile.render(tuning_data)

    return tuned_profile


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
    tmp_data = yaml.load(scratch_profile)
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
