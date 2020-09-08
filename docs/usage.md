# Usage

Configuration for YamlConfiger is specified in a *template*.
This is a directory containing files using the Jinja 2 template syntax.

To generate a configuration, specify a *profile* containing values substituted into the template.
The profile is represented as a directory containing YAML files.

## User (CLI) guide

```bash
yacgf --help

yacgf --list-profiles
yacgf --list-templates

# perform a generation of a default profile
yacgf --profile artemis/2.5.0/default.yaml
# also save result to [OUTDIR] directory
yacgf --profile [PROFILE] --output [OUTDIR]
```
