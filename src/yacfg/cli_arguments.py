import argparse
import json
import re
from typing import Dict, List, Tuple, Union

from . import DESCRIPTION, NAME, __version__

REX_BOOL_TRUE = re.compile(r"^(([Tt][Rr][Uu][Ee])|[Yy][Ee][Ss]|(1)|[Oo][Nn])$")
REX_BOOL_FALSE = re.compile(r"^(([Ff][Aa][Ll][Ss][Ee])|([Nn][Oo])|(0)|[Oo][Ff][Ff])$")


def boolize(data: str) -> Union[bool, None]:
    """Convert input values from string to bool if possible

    :param data: input data from argparse
    :type data: str
    :return: converted boolean value, or None if not specified
    :rtype: bool or None

    :raises ValueError: if conversion failed
    """
    if data is None:
        return None
    if REX_BOOL_TRUE.match(data):
        return True
    if REX_BOOL_FALSE.match(data):
        return False
    raise ValueError(f"Cannot convert input option {data} to bool")


def split_key_value(item: str) -> Tuple[str, str]:
    """Split KEY=VALUE specifier or raise a ValueError exception.

    :param item: input KEY=VALUE string option.
    :type item: str

    :raises ValueError: if cannot split

    :return: pair of split key and value
    :rtype: str, str
    """
    try:
        key, value = item.split("=", 1)
    except ValueError:
        raise ValueError(f'Missing KEY=VALUE pair in option "{item}"')
    return key, value


def parse_key_value_list(items: List[Dict[str, str]]) -> Dict[str, str]:
    """Convert a list of dictionaries into a single dictionary.

    :param items: List of dictionaries.
    :type items: list[dict]

    :return: Merged dictionary with key-value pairs from all dictionaries.
    :rtype: dict
    """
    return {k: v for item in items for k, v in item.items() if isinstance(item, dict)}


parser = argparse.ArgumentParser(
    prog="{} {}".format(NAME, __version__),
    description=DESCRIPTION,
    epilog="The Cake is a lie.",
)

# Group Main
group_main = parser.add_argument_group(title="Main options")

group_main.add_argument(
    "-t",
    "--template",
    help="Configuration template set name (packaged, or user provided path)",
)

group_main.add_argument(
    "-p",
    "--profile",
    help="Configuration data profile name (packaged, or user provided path)",
)

group_main.add_argument("-o", "--output", help="Output path to generated files to")

group_main.add_argument(
    "--tune",
    help=(
        "Fine tune profile variables by providing a YAML file"
        " with values mapping (if selected profile support variables)"
    ),
    action="append",
)

group_main.add_argument(
    "--opt",
    metavar="KEY=VALUE",
    help=(
        "Fine tune one tuning value format KEY=VALUE, has higher"
        " priority than tuning files."
    ),
    action="append",
)

# Group Extra
group_extra = parser.add_argument_group(title="Extra Options")

group_extra.add_argument(
    "--extra-properties",
    help="Extra properties (key-value pairs) that can be used by specific templates"
    ' Example: "{x:y,a:b}"',
    type=json.loads,
)

group_extra.add_argument(
    "-f",
    "--filter",
    help="Regular expression enabled output filename filter,"
    " to generate_via_tuning_files only selected config files",
    action="append",
)

group_extra.add_argument(
    "--save-effective-profile",
    help="Write used profile data to output directory," " output has to be specified",
    action="store_true",
)

# Group Render
group_render = parser.add_argument_group(title="Render options")

group_render.add_argument(
    "--render-generator-notice",
    help="Control generator notice (header) to be put into output files"
    " (True/False)",
)

group_render.add_argument(
    "--render-licenses",
    help="Control licenses to be put into output files (True/False)",
)

# Group Query
group_query = parser.add_argument_group(title="Query options")

group_query.add_argument(
    "--list-templates", help="Print a list of packaged templates", action="store_true"
)

group_query.add_argument(
    "--list-profiles", help="Print a list of packaged profiles", action="store_true"
)

# Group Creator
group_creator = parser.add_argument_group(
    title="Creator Options",
)

group_creator.add_argument(
    "--new-profile",
    help="Export a local copy of an existing profile for further editing"
    " (local path), you need to use profile option to select a profile",
)

group_creator.add_argument(
    "--new-profile-static",
    help="Export a local copy of a static version of an existing profile"
    " for further editing (local path), you need to use profile"
    " option to select a profile",
)

group_creator.add_argument(
    "--new-template",
    help="Export a local copy of selected template for further editing"
    " (local path), you need to use template to select a template",
)

group_creator.add_argument(
    "--export-tuning",
    help="Export a local copy of profile available variables in yaml"
    " for easy creation of tuning file (local path)",
)

# Group Logging
group_logging = parser.add_argument_group(title="Logging options")

group_logging.add_argument(
    "-q",
    "--quiet",
    help="Keep output to minimum, only requested data (listing) or errors",
    action="store_true",
)

group_logging.add_argument(
    "-v",
    "--verbose",
    help="Print generation status and user relevant info",
    action="store_true",
)

group_logging.add_argument(
    "-d", "--debug", help="Print debugging details", action="store_true"
)

# Group Misc
group_misc = parser.add_argument_group(title="Miscellaneous")

group_misc.add_argument(
    "--version", help="Display version information", action="store_true"
)

args = parser.parse_args()
