# amqcfg - AMQ configurator

This tool can generate a set of configuration files mainly needed for
AMQ Broker, but it is not limited to only generating files for one product.

It has a user facing Command Line Tool for quick and easy command line usage.
Furthermore it is possible to its API to use it in your python code.

## Getting started

* python 3.5+ or python2.7
* current requirements from setup.py (runtime requirements only)
* python virtualenv recommended (install via system package manager
or `pip install --user virtualenv`)

for contributors:
* requirements from requirements.txt (there are Dev and QA requirements as well)

### From git

```bash
git clone git@bitbucket.org:msgqe/amqcfg.git
python -m virtualenv -p python3 venv3
source venv3/bin/activate
./setup.py install
amqcfg --help
```

### From PiPy

```bash
python -m virtualenv -p python3 venv3
source venv3/bin/activate
pip install amqcfg
amqcfg --help
```

## User (CLI) guide

```bash
amqcfg --help

amqcfg --list-profiles
amqcfg --list-templates

# perform a generation of a default profile
amqcfg --profile artemis/2.5.0/default.yaml
# also save result to [OUTDIR] directory
amqcfg --profile [PROFILE] --output [OUTDIR]
```

## Customization

Quickest way to customize data is to use hot-variables, basically variables
that profile itself provides for tuning. Next step is to write (modify) custom
profile with completely custom values.
And if that does not satisfy your needs, then custom template might be required.

### Profile tuning

Simply export tuning values from profile you want to tune and change those you
need to change. Then supply tuning file when generating.

```bash
amqcfg --profile [PROFILE] --export-tuning my_values.yaml
vim my_values.yaml
amqcfg --profile [PROFILE] --tune my_values.yaml

# multiple tuning files can be overlaid
# they are updated in sequence, only values present are overwritten
amqcfg --profile [PROFILE] --tune my_values.yaml --tune machine_specific.yaml \
       --tune logging_debug.yaml --output [OUTDIR]
```

## Custom profiles

Write your own, or simply export existing profile and modify that.

You can export dynamic version with includes of some modules, that would still
 work. Either you can use imports from package, or your own local files.

Or you can export completely rendered profile file without any includes or
variables and modify that as you like.


```bash
# export profile with dynamic includes
amqcfg --profile [PROFILE] --new-profile my_new_profile.yaml
# export completely generated profile
amqcfg --profile [PROFILE] --new-profile-static my_new_profile.yaml
vim my_new_profile.yaml
amqcfg --profile my_new_profile.yaml
```

## Custom templates

And last resort is to export template and modify that. But remember template,
or more correctly template set is a directory containing a set of main
templates that subsequently generate a new file.

Of course feel free to write your own templates. Especially when you need to
generate files for something that is not packaged.

Just remember for template set to be identified the directory must contain
a file named '_template' and then main templates ending with '.jinja2'.

```bash
amqcfg --template [TEMPLATE] --new-template my_new_template
vim my_new_template/[MAIN_TEMPLATES].jinja2
amqcfg --template my_new_template --profile [PROFILE]

```

## API guide

Direct use of API is to use `generate()` nearly the same as the CLI.

```python
import amqcfg

# generate files as above CLI exaple to output directory
amqcfg.generate(
    profile='artemis/2.5.0/default.yaml',
    tuning_files=[
        'my_values.yaml',
        'machine_specific.yaml',
        'logging_debug.yaml'
    ],
    output_path='/opt/artemis-2.5.0-i0/etc/',
)

# just get generated data for further processing
data = amqcfg.generate(
    profile='artemis/2.5.0/default.yaml',
    tuning_files=[
        'my_values.yaml',
        'machine_specific.yaml',
        'logging_debug.yaml'
    ],
)
print(data['broker.xml'])
```

More API oriented changes will be done in future versions, for now development
was focused on user facing CLI. And functions used by CLI is not optimal for
use in another code.

What is definitely needs to be done:
*   `generate` alternative that will use profile data directly from variable

## Documentation

this readme and docstrings, for now. Sorry about that.

I would like to have [readthedocs.org](http://readthedocs.org) documentation.

## Contributing

If you find a bug or room for improvement, submit either a ticket or PR.

## Contributors

_Alphabetically ordered_

* Zdenek Kraus <zkraus@redhat.com>

## License

Copyright 2018 Red Hat Inc.

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
