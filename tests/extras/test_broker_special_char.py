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


def test_with_special_chars(*_):
    print("testing 1")
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

