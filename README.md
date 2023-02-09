# yacfg - YAML Configurator

This tool can generate a set of configuration files mainly created for
ActiveMQ Artemis, but it is not limited to only generating configuration files.

It has a user facing Command Line Tool for quick and easy command line usage.
Furthermore, it is possible to use its API in your python code.

## Getting started

* Python 3.7+
* Python Poetry

### From git

```bash
git clone git@github.com:rh-messaging-qe/yacfg.git
poetry install
yacfg --help
```

### From PyPI

```bash
pip install yacfg
yacfg --help
```

## User (CLI) guide

```bash
yacfg --help

# Set path for profiles and templates
# For example the ActiveMQ Artemis template and profiles
git clone https://github.com/rh-messaging-qe/yacfg_artemis.git ./yacfg_artemis

# Currently is needed to setup profiles and templates paths as environment variables
export YACFG_PROFILES=./yacfg_artemis/profiles
export YACFG_TEMPLATES=./yacfg_artemis/templates

yacfg --list-profiles
yacfg --list-templates

# perform a generation of a default profile
yacfg --profile artemis/default.yaml.jinja2

# also save result to [OUTDIR] directory
yacfg --profile [PROFILE] --output [OUTDIR]
```

## Customization

Quickest way to customize data is to use hot-variables, basically variables
that the profile itself provides for tuning. Next step is to write (modify) custom
profile with completely custom values.
If that does not satisfy your needs, then a custom template might be required.

### Profile tuning

Simply export tuning values from profile you want to tune and change those you
need to change. Then supply the custom tuning file(s) when generating the profile.

```bash
yacfg --profile [PROFILE] --export-tuning my_values.yaml
vim my_values.yaml
yacfg --profile [PROFILE] --tune my_values.yaml

# multiple tuning files can be overlaid
# they are updated in sequence, only values present are overwritten
yacfg --profile [PROFILE] --tune my_values.yaml --tune machine_specific.yaml \
       --tune logging_debug.yaml --output [OUTDIR]
```

## Custom profiles

Write your own, or simply export an existing profile and modify that.

You can export dynamic version with includes of some modules, that would still
 work. Either you can use imports from package, or your own local files.

Or you can export completely rendered profile file without any includes or
variables and modify that as you like.


```bash
# export profile with dynamic includes still active jinja2 files
yacfg --profile [PROFILE] --new-profile my_new_profile.yaml.jinja2
# export completely generated profile without any jinja2 fields, plain yaml
yacfg --profile [PROFILE] --new-profile-static my_new_profile.yaml
vim my_new_profile.yaml
yacfg --profile my_new_profile.yaml
```

Profile is just another jinja2 file that enables customization of profile data
 -- that is tuning. Because of that we recommend keeping the extension `.yaml.jinja2`
 unless it is static profile without any jinja2 capabilities, in that case it could
 be named `.yaml`. That way we can run yaml lint against static profiles and verify
 that they are correct.

 All profiles have to be used to generate files without any tuning. That means,
 if they are tune-able, they have to contain all default values in `_defaults` section.
 That section is also used for tuning, so any variable in there will be exported as tuning.

## Custom templates

The last resort is to export a template and modify that. But remember a template,
or more correctly a template set is a directory containing a set of main
templates that subsequently generate_via_tuning_files a new file.

Of course feel free to write your own templates. Especially when you need to
generate_via_tuning_files for something that is not packaged.

Just remember for a template set to be identified the directory must contain
a file named '_template' and then main templates ending with '.jinja2'.

```bash
yacfg --template [TEMPLATE] --new-template my_new_template
vim my_new_template/[MAIN_TEMPLATES].jinja2
yacfg --template my_new_template --profile [PROFILE]

```

## Jinja2 filters:

We use Jinja2 filters from Ansible project, read more about it here: 
[https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html](Ansible filters documentation)

## API guide

Direct use of API is to use `generate()` nearly the same as the CLI.
With option to use tuning values directly.

Tuning data will be overlaid in order of appearance, using python
dict.update(), so values that will appear later will overwrite previous
values. We recommend that tuning values are always flat, because update
is not recursive. The same applies for data from tuning files as well
as the directly provided data.

Data application order:

- profile defaults
- data from tuning files (in order of appearance) `tuning_files_list`
- data provided directly (in order of appearance) `tuning_data_list`


```python
import yacfg

# generating only broker.xml config using default values from profile,
# no tuning, writing output to a target path
yacfg.generate(
    profile='artemis/default.yaml.jinja2',
    output_filter=['broker.xml'],
    output_path='/opt/artemis-i0/etc/',
)

# using both files and direct values, and writing generated configs to
# a target directory
yacfg.generate(
    profile='artemis/default.yaml.jinja2',
    tuning_files_list=[
        'my_values.yaml',
        'machine_specific.yaml',
        'logging_debug.yaml'
    ],
    tuning_data_list=[
        {'name': 'custom name', 'config': 'option_a'},
        {'address': '10.0.0.1'},
        {'LOG_LEVEL': 'debug'},
    ],
    output_path='/opt/artemis-i0/etc/',
)

# just get generated data for further processing, using just tuning files
data = yacfg.generate(
    profile='artemis/default.yaml.jinja2',
    tuning_files_list=[
        'my_values.yaml',
        'machine_specific.yaml',
        'logging_debug.yaml'
    ],
)
print(data['broker.xml'])
```

## Batch configurations

In case you have multiple services to configure in your environment,
that you probably will have at some point, there is a tool for that
as well. The tool is called yacfg-batch. It has only yaml input, and
it uses yacfg to generate configurations as you are already used to.

Input yaml file defines all services you need to generate, what
profiles to use, and what tuning to provide to `yacfg`.
It allows you to configure defaults and common for services.

### Batch profile file

As said it is YAML. It has two special sections: `_default` and `_common`.
As the name suggests, `_default` values are used when values are not
defined per specific section. Where `_common` is added to the values
of all sections. The important thing here is that `_default` has lower
priority than `_common` and that has lower priority than specific section
values.

Every section has 4 values: `profile`, `template`, `tuning_files`,
 and `tuning`. As the name suggests, `profile` defines what generation profile
 to select, and it directly correlates with `yacfg`'s `--profile`.
 `template` defines what generation template to use
 (overrides one in the profile if defined), and it directly correlates with
 `--template` from `yacfg`. `tuning_files` option is a list of tuning
 files to use, when combining defaults, commons, and specific values,
 tuning_files list is concatenated. Finally `tuning` is a map of
 specific tuning values, correlates with `--opt` of `yacfg`. When combining
 defaults, commons, and specifics, it will be updated over using python
 dict.update() and it will work only on first level, so it is recommended
 to use flat values for tuning only.

#### Example
```yaml

_default:
    profile: artemis/default.yaml.jinja2
    tuning_files:
      - defaults/broker_default.yaml

_common:
    tuning_files:
      - common/security.yaml
      - common/logging.yaml
    tuning_values:
      LOG_LEVEL_ALL: INFO

brokerA/opt/artemis/etc:
    pass: true

brokerB/opt/artemis/etc:
    profile: artemis/AIOBasic.yaml.jinja2
    tuning_files:
      - brokerB/queues.yaml

---

_default:
    profile: artemis/default.yaml.jinja2
    tuning_files:
      - defaults/broker_default.yaml

brokerC/opt/amq/etc:
    tuning:
      LOG_LEVEL_ALL: DEBUG

```

As you can see, `yacfg-batch` supports multiple sections, in single
batch profile file, that allows you to generate multiple groups using
separated `_default` and `_common` sections for that.

#### Executing batch

When you have defined all tuning files you need, and in the root of this
batch configuration you have your batch profile file, you can now simply
run `yacfg-batch`:

```bash

yacfg-batch --input [batch_profile_file] --output [output_path]
```

You can use multiple input files and all of those will be generated
consecutively. In the output path, new subdirectories will be created
for every item you configure (every section), section key will be used
for that subdirectory. If the section name resembles a path, whole
path will be created. For example for `brokerA/opt/artemis/etc`
the configuration will be generated into
`[output_path]/brokerA/opt/artemis/etc/`.

## Documentation
Formatted documentation can be viewed at [rh-messaging-qe.github.io/yacfg/](https://rh-messaging-qe.github.io/yacfg/).


## Contributing

If you find a bug or room for improvement, submit either a ticket or PR.

## Contributors

_Alphabetically ordered_

* Dominik Lenoch <dlenoch@redhat.com> (maintainer)
* Michal Tóth <mtoth@redhat.com>
* Otavio Piske <opiske@redhat.com>
* Sean Davey <sdavey@redhat.com>
* Zdenek Kraus <zkraus@redhat.com> (author)

## License

Copyright 2018-2021 Red Hat Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Acknowledgments

* [jinja2](http://jinja.pocoo.org/docs/2.10/) -- awesome templating engine
* [yaml](http://yaml.org/) -- very convenient user readable format
* [learn_yaml](https://learnxinyminutes.com/docs/yaml/) -- great YAML cheat sheet
* [pyyaml](https://github.com/yaml/pyyaml) -- python YAML parser
* [jq](https://stedolan.github.io/jq/) -- great tool for working with structured data (JSON)
* [yq](https://yq.readthedocs.io/en/latest/) -- YAML variant of jq
* [github templates examples](https://github.com/stevemao/github-issue-templates/tree/master/simple) -- Nice set of ISSUE_TEMPLATE.md and PULL_REQUESTS_TEMPLATE.md examples
* [contributing example](https://gist.github.com/PurpleBooth/b24679402957c63ec426) -- example/template of CONTRIBUTING.md
* [Fedora Project code-of-conduct](https://docs.fedoraproject.org/en-US/project/code-of-conduct/) -- the inspiration for CODE_OF_CONDUCT.md
