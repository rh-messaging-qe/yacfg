# Usage

Configuration templates are specified in a *template*.
This is a directory containing files using the Jinja 2 template syntax.

To generate a configuration, specify a *profile* containing values substituted into the template.
The profile is represented as a directory containing Jinja 2 or YAML files.
Profiles are in fact data templates to enable easy cutomization for the user, and because of
that profiles are jinja2 as well. They can be YAML if they are static.
 But in the end they become YAML files and are used as data source for templates.

## User (CLI) guide

```bash
yacgf --help

yacgf --list-profiles
yacgf --list-templates

# perform a generation of a default profile
yacgf --profile artemis/2.5.0/default.yaml.jinja2
# also save result to [OUTDIR] directory
yacgf --profile [PROFILE] --output [OUTDIR]
```
