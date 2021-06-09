# Batch configurations

In case you have multiple services to configure in your environment,
that you probably will have at some point, there is a tool for that
as well. The tool is called yacfg-batch. It has only yaml input and
it uses yacfg to generate configurations as you are already used to.

Input yaml file defines all services you need to generate, what
profiles to use, and what tuning to provide to `yacfg`.
It allows you to configure defaults and common for services.

## Batch profile file

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

Example:
```yaml

_default:
    profile: artemis/2.5.0/default.yaml.jinja2
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
    profile: artemis/2.5.0/AIOBasic.yaml.jinja2
    tuning_files:
      - brokerB/queues.yaml

---

_default:
    profile: amq_broker/7.2.0/default.yaml.jinja2
    tuning_files:
      - defaults/amq_broker_default.yaml

brokerC/opt/amq/etc:
    tuning:
      LOG_LEVEL_ALL: DEBUG

```

As you can see, `yacfg-batch` supports multiple sections, in single
batch profile file, that allows you to generate multiple groups using
separated `_default` and `_common` sections for that.

## executing batch

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
