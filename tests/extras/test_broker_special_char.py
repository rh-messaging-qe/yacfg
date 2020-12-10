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

import yacfg
import shutil
import os


def test_with_special_chars(*_):
    print("tesing 1")
    tune_file = 'extras/tune_files/special_address_setting.yaml'

    profile = 'artemis/2.16.0/default_with_user_address_settings.yaml.jinja2'
    tuning_files = [tune_file]
    extra_props = {'uuid1':'','uuid2':'OFF'}
    output = 'etc'

    yacfg.generate(
        profile=profile,
        tuning_files_list=tuning_files,
        extra_properties_data=extra_props,
        output_path=output
    )

    broker_xml = output + '/broker.xml'
    file1 = open(broker_xml, 'r')
    try:
        lines = file1.readlines()

        empty_found = False
        off_found = False
        for ln in lines:
            if ln.find('<dead-letter-queue-prefix></dead-letter-queue-prefix>') != -1:
                empty_found = True
            if ln.find('<config-delete-queues>OFF</config-delete-queues>') != -1:
                off_found = True

        assert empty_found is True
        assert off_found is True

    finally:
        file1.close()
        shutil.rmtree(output)


def trim_empty_lines(lines):
    new_lines = []
    for l in lines:
        if len(l.strip()) > 0:
            new_lines.append(l)
    return new_lines


def test_logging_with_special_chars(*_):

    print("testing 2")
    tune_file = 'extras/tune_files/special_logging_setting.yaml'
    result_file = 'extras/results/special_logging_setting_result.yaml'

    profile = 'artemis/2.16.0/default_with_user_address_settings.yaml.jinja2'
    tuning_files = [tune_file]
    extra_props = {'ac_log_level_root':'OFF','uniid':'OFF','uniid1':'OFF','uniid2':'ON','uniid3':'OFF','uniid4':'YES'}
    output = 'etc'

    yacfg.generate(
        profile=profile,
        tuning_files_list=tuning_files,
        extra_properties_data=extra_props,
        output_path=output
    )

    logging_properties = output + '/ac.logging.properties'
    file1 = open(logging_properties, 'r')
    file2 = open(result_file, 'r')
    try:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

        result1 = trim_empty_lines(lines1)
        result2 = trim_empty_lines(lines2)

        assert len(result1) == len(result2)
        length = len(result1)
        for i in range(length):
            assert result1[i] == result2[i]
    finally:
        file1.close()
        file2.close()
        shutil.rmtree(output)
