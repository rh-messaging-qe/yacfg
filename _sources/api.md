# API guide

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
    profile='artemis/2.5.0/default.yaml',
    output_filter=['broker.xml'],
    output_path='/opt/artemis-2.5.0-i0/etc/',
)

# using both files and direct values, and writing generated configs to
# a target directory
yacfg.generate(
    profile='artemis/2.5.0/default.yaml',
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
    output_path='/opt/artemis-2.5.0-i0/etc/',
)

# just get generated data for further processing, using just tuning files
data = yacfg.generate(
    profile='artemis/2.5.0/default.yaml',
    tuning_files_list=[
        'my_values.yaml',
        'machine_specific.yaml',
        'logging_debug.yaml'
    ],
)
print(data['broker.xml'])
```
