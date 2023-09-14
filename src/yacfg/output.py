import logging
import os
import shutil
from typing import Any, Dict, List, Optional

import yaml

from . import NAME, exceptions, files, profiles

LOG: logging.Logger = logging.getLogger(NAME)


class MyDumper(yaml.SafeDumper):
    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        return super().increase_indent(flow, False)


def yaml_dump_wrapper(data: Dict[str, Any]) -> str:
    """
    Wrapper function for dumping YAML data with custom settings.

    :param data: Data to be dumped as YAML.
    :type data: dict
    :return: Dumped YAML data as a string.
    :rtype: str
    """
    return yaml.dump(
        data=data,
        Dumper=MyDumper,
        default_flow_style=False,
        explicit_start=True,
        explicit_end=False,
        width=140,
    )


def new_profile(profile: str, dest_profile: str) -> None:
    """
    Export an existing profile to a new destination.

    :param profile: Existing profile name (from user or packaged).
    :type profile: str
    :param dest_profile: Filename of the new profile.
    :type dest_profile: str
    :raises OSError: If there is a problem with the destination path.
    """
    profile_name, profile_path = files.select_profile_file(profile)
    src: str = os.path.join(profile_path, profile_name)

    dest_path: str = os.path.dirname(dest_profile)
    if dest_path:
        files.ensure_output_path(dest_path)

    shutil.copyfile(src, dest_profile)


def new_profile_rendered(
    profile: str,
    dest_profile: str,
    tuning_files: Optional[List[str]] = None,
    tuning_data_list: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """
    Export an existing profile in static form, stripped defaults section.

    :param profile: Existing profile name (from user or packaged).
    :type profile: str
    :param dest_profile: Filename of the new profile.
    :type dest_profile: str
    :param tuning_files: User-specified tuning file path, defaults to None.
    :type tuning_files: list[str], optional
    :param tuning_data_list: User-specified tuning data list provided directly, defaults to None.
    :type tuning_data_list: list[dict], optional
    :raises OSError: If there is a problem with the destination path.
    """
    config_data, _ = profiles.get_tuned_profile(profile, tuning_files, tuning_data_list)

    dest_path: str = os.path.dirname(dest_profile)
    dest_name: str = os.path.basename(dest_profile)
    if dest_path:
        files.ensure_output_path(dest_path)

    config_data.pop("_defaults", None)

    export_data: str = yaml_dump_wrapper(config_data)

    export_data = (
        f"# {NAME} tuning file generated from profile {profile}\n{export_data}"
    )
    write_output(dest_name, dest_path, export_data)


def new_template(template: str, dest_template: str) -> None:
    """
    Export an existing template directory to a new destination.

    :param template: Existing template name (from user or packaged).
    :type template: str
    :param dest_template: Directory name of the new template.
    :type dest_template: str
    :raises OSError: If there is a problem with the destination path.
    """
    template_path = files.select_template_dir(template)
    shutil.copytree(template_path, dest_template, symlinks=False)


def export_tuning_variables(profile_name: str, dest_file: str) -> None:
    """
    Export a subsection of profile's tunable variables to a new YAML file.

    :param profile_name: Profile name (user-defined or packaged).
    :type profile_name: str
    :param dest_file: Filename of the destination tuning file.
    :type dest_file: str
    :raises OSError: If there is a problem with the destination path.
    :raises ProfileError: If there is a problem with the selected profile.
    """
    defaults_data = profiles.load_profile_defaults(profile_name)
    if not defaults_data:
        raise exceptions.ProfileError(
            f'Selected profile "{profile_name}" does not contain any tunable variables'
        )

    dest_path: str = os.path.dirname(dest_file)
    dest_name: str = os.path.basename(dest_file)
    if dest_path:
        files.ensure_output_path(dest_path)

    export_data: str = yaml_dump_wrapper(defaults_data)

    LOG.debug(f"Exported tuning data:\n{export_data}")
    export_data = (
        f"# {NAME} tuning file generated from profile {profile_name}\n{export_data}"
    )
    write_output(dest_name, dest_path, export_data)
    LOG.info("Tuning data exported")


def write_output(filename: str, output_path: str, content: str) -> None:
    """
    Write content to the specified file.

    :param filename: Name of the file.
    :type filename: str
    :param output_path: Path to the output directory.
    :type output_path: str
    :param content: Content to write to the file.
    :type content: str
    :raises OSError: If there is a problem with the output path or writing the file.
    """
    output_file = os.path.join(output_path, filename)
    try:
        with open(output_file, "w") as file:
            file.write(content)
        LOG.debug(f"Successfully wrote content to {output_file}")
    except OSError as e:
        raise OSError(f"Error writing content to {output_file}: {e}") from e
