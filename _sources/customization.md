# Customization

Quickest way to customize data is to use hot-variables, basically variables
that the profile itself provides for tuning. Next step is to write (modify) custom
profile with completely custom values.
If that does not satisfy your needs, then a custom template might be required.

## Profile tuning

Simply export tuning values from profile you want to tune and change those you
need to change. Then supply the custom tuning file(s) when generating the profile.

```bash
yacgf --profile [PROFILE] --export-tuning my_values.yaml
vim my_values.yaml
yacgf --profile [PROFILE] --tune my_values.yaml

# multiple tuning files can be overlaid
# they are updated in sequence, only values present are overwritten
yacgf --profile [PROFILE] --tune my_values.yaml --tune machine_specific.yaml \
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
 -- that is tuning. Becuase of that we recommend to keep the extension `.yaml.jinja2`
 unless it is static profile withou any jinja2 capabilities, in that case it could
 be named `.yaml`. That way we can run yaml lint against static profiles and verify
 that they are correct.

 All profiles have to be used to generate files without any tuning. That means,
 if they are tune-able, they have to contain all default values in `_defaults` section.
 That section is also used for tuning, so any variable in there will be exported as tuning.

# Custom templates

The last resort is to export a template and modify that. But remember a template,
or more correctly a template set is a directory containing a set of main
templates that subsequently generate_via_tuning_files a new file.

Of course feel free to write your own templates. Especially when you need to
generate_via_tuning_files files for something that is not packaged.

Just remember for a template set to be identified the directory must contain
a file named '_template' and then main templates ending with '.jinja2'.

```bash
yacgf --template [TEMPLATE] --new-template my_new_template
vim my_new_template/[MAIN_TEMPLATES].jinja2
yacgf --template my_new_template --profile [PROFILE]

```
