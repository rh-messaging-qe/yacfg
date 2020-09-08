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

from __future__ import print_function

import copy
import logging
import os

import yaml

import yacfg.yacfg
from .exceptions import YacfgBatchException

LOG = logging.getLogger(__name__)


class GenerateData(object):
    profile_name = None
    template_name = None
    tuning_files = None
    tuning_data = None

    def __str__(self):
        tmp = (
            'GenerateData({!r}, {!r}, {}, {})'.format(
                self.profile_name,
                self.template_name,
                self.tuning_files,
                self.tuning_data
            )
        )
        return tmp

    __repr__ = __str__

    def __eq__(self, other):
        return (self.profile_name == other.profile_name
                and self.template_name == other.template_name
                and self.tuning_files == other.tuning_files
                and self.tuning_data == other.tuning_data)


def iter_gen_profiles(filename):
    # noinspection PyUnusedLocal
    profile_data_list = None

    try:
        profile_data_list = yaml.load_all(open(filename, 'r'))
    except IOError as exc:
        raise YacfgBatchException(
            'Unable to open gen profile "{}" {}'.format(filename, exc)
        )
    except yaml.YAMLError as exc:
        raise YacfgBatchException(
            'Unable to parse YAML gen profile "{}" {}'.format(filename, exc)
        )

    for profile_data in profile_data_list:
        yield profile_data


def generate(input_files, output_path=None):
    """Main batch generation function, get input files, collects data,
    and uses core yacfg's generate to do the work.

    :param input_files: list of yaml input files with generation
        specification
    :type input_files: list[str]
    :param output_path: path to write generated configurations
    :type output_path: str | None
    """
    for profile_file in input_files:
        LOG.info('- Profile file: {}'.format(profile_file))
        for profile_file_data in iter_gen_profiles(profile_file):
            input_path = os.path.dirname(profile_file)

            default = extract_generate_data(profile_file_data)
            common = extract_generate_data(profile_file_data, '_common')

            generate_all_profiles(
                input_path, output_path, default, common, profile_file_data
            )


def extract_generate_data(profile_file_data, section='_default'):
    """Get all relevant data from special sections like _default

    Data contains profile name, template name, tuning files, and
    tuning data.

    :param profile_file_data: one chunk of batch generation profile
        that is supposed to contain the section
    :type profile_file_data: dict
    :param section: selected section name, default: '_default'
    :type section: str

    :return: Extracted generate data
    :rtype: GenerateData
    """
    section_data = profile_file_data.get(section)
    result = GenerateData()
    if section_data:
        result.profile_name = section_data.get('profile')
        result.template_name = section_data.get('template')
        result.tuning_files = section_data.get('tuning_files')
        result.tuning_data = section_data.get('tuning')
    return result


def prioritize_generate_data(profile, common, default):
    """Gather all available generation data by their priority,
    the highest is the particular profile data, then defaults.
    Common data will be shared even if profile data are available.
    Be aware that with tuning_files and tuning_data, Default has lower
    priority than Common, so if Profile data is not present, Default
    will be applied before common.

    With profile name and template name is priority order:
        profile, common, default
    there is no sharing, since those are single values.

    :param profile: profile relevant generate data
    :type profile: GenerateData
    :param common: common generate data
    :type common: GenerateData
    :param default: default generate data
    :type default: GenerateData

    :return: prioritized data in generate data format
    :rtype: GenerateData
    """
    result = GenerateData()

    for key in ['profile_name', 'template_name']:
        for conf in [default, common, profile]:
            value = getattr(conf, key)
            if value:
                setattr(result, key, value)

    # tuning files
    result.tuning_files = []
    if not profile.tuning_files and default.tuning_files:
        result.tuning_files.extend(default.tuning_files)
    if common.tuning_files:
        result.tuning_files.extend(common.tuning_files)
    if profile.tuning_files:
        result.tuning_files.extend(profile.tuning_files)
    # normalize empty list to None
    if not result.tuning_files:
        result.tuning_files = None

    # tuning data
    result.tuning_data = {}
    if not profile.tuning_data and default.tuning_data:
        result.tuning_data = copy.copy(default.tuning_data)
    if common.tuning_data:
        result.tuning_data.update(common.tuning_data)
    if profile.tuning_data:
        result.tuning_data.update(profile.tuning_data)
    # normalize empty dict to none
    if not result.tuning_data:
        result.tuning_data = None

    return result


def generate_all_profiles(input_path, output_path, default, common,
                          profiles_file_data):
    """Main subroutine for generating all service's profile configs.

    :param input_path: path of used input yaml file, to pick
        dependencies, tuning files, etc.
    :type input_path: str
    :param output_path: path where to generate configs, name of service
        profile will be used as subdirectory
    :type output_path: str
    :param default: collection of default GenerateData
    :type default: GenerateData
    :param common: collection of common GenerateData
    :type common: GenerateData
    :param profiles_file_data: profiles generation data in dict format,
        as loaded from YAML
    :type profiles_file_data: dict
    """
    profile_list = [
        x for x in profiles_file_data.keys() if not x.startswith('_')
    ]

    for profile in profile_list:
        LOG.info('-- Profile: {}'.format(profile))

        profile_data = extract_generate_data(profiles_file_data, profile)
        generate_data = prioritize_generate_data(profile_data, common, default)

        if not generate_data.profile_name:
            raise YacfgBatchException(
                'No selected profile,'
                ' cannot generate_via_tuning_files.'
            )

        # post process tuning files
        if generate_data.tuning_files:
            generate_data.tuning_files = [
                os.path.join(input_path, x) for x in generate_data.tuning_files
            ]

        LOG.debug('tuning data: {}'.format(generate_data.tuning_data))

        target_path = None
        if output_path:
            target_path = os.path.join(output_path, profile)

        tuning_data = None
        if generate_data.tuning_data:
            tuning_data = [generate_data.tuning_data]

        LOG.debug(
            'CALL: yacfg --profile {} --template {} '
            '--tuning {} --output {} # extra tuning: {} '
            '>> {}'.format(
                generate_data.profile_name, generate_data.template_name,
                generate_data.tuning_files, target_path,
                generate_data.tuning_data, target_path
            ))

        yacfg.yacfg.generate(
            profile=generate_data.profile_name,
            template=generate_data.template_name,
            output_path=target_path,
            tuning_files_list=generate_data.tuning_files,
            tuning_data_list=tuning_data,
        )
