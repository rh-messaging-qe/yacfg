import itertools
import logging
import os
from typing import Dict, List, Optional, Tuple, Union

import yaml
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, Template

from . import NAME
from .exceptions import ProfileError, TemplateError
from .files import get_profiles_paths, select_profile_file

LOG: logging.Logger = logging.getLogger(NAME)


def load_tuning_files(tuning_files: Optional[List[str]] = None) -> List[Dict[str, str]]:
    """Load tuning data from requested tuning files in order and
    provide a list of tuning data for further processing.

    :param tuning_files: List of tuning file names.
    :type tuning_files: list[str]

    :return: List of tuning data loaded from YAML tuning files.
    :rtype: list[dict]
    """
    tuning_values_list: List[Dict] = []

    if tuning_files:
        for tuning_file in tuning_files:
            try:
                with open(tuning_file, "r") as stream:
                    tuning_values_list.append(yaml.safe_load(stream))
            except IOError as exc:
                raise ProfileError(
                    'Unable to open tuning file "{}" {}'.format(tuning_file, exc)
                )
            except yaml.YAMLError as exc:
                raise ProfileError(
                    'Unable to parse YAML tuning file "{}" {}'.format(tuning_file, exc)
                )

            LOG.debug("Tuning file {} loaded".format(tuning_file))
    else:
        LOG.debug("No tuning files requested.")

    return tuning_values_list


def load_tuning(
    profile_defaults: Dict[str, str] = {},
    tuning_files_list: Optional[List[str]] = None,
    tuning_data_list: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, str]:
    """Load and apply all tuning, from profile defaults, tuning
    files, and then directly provided tuning data. All data is
    applied in order.

    :param profile_defaults: Profile defaults data to be tuned.
    :type profile_defaults: dict, optional
    :param tuning_files_list: List of tuning file names.
    :type tuning_files_list: list[str], optional
    :param tuning_data_list: List of tuning data directly provided.
    :type tuning_data_list: list[dict], optional

    :return: Compound overlaid tuning data in order of appearance.
    :rtype: dict
    """
    result: Dict = {}
    files_tuning_values: List[Dict] = load_tuning_files(tuning_files_list)
    if profile_defaults:
        result.update(profile_defaults)
    if tuning_data_list is None:
        tuning_data_list = []

    for tuning_data in itertools.chain(files_tuning_values, tuning_data_list):
        result.update(tuning_data)

    return result


def get_tuned_profile(
    profile: str,
    tuning_files_list: Optional[List[str]] = None,
    tuning_data_list: Optional[List[Dict[str, str]]] = None,
) -> Tuple[Dict[str, str], str]:
    """Get selected profile and use tuning data to fine-tune
    its variable values.

    :param profile: Profile name (packaged) or path to profile
        (user-specified).
    :type profile: str
    :param tuning_files_list: List of files with tuning data to be used.
    :type tuning_files_list: list[str], optional
    :param tuning_data_list: Data used to tune the variable values.
    :type tuning_data_list: list[dict], optional

    :raises ProfileError: When the tuned profile is not valid.

    :return: Compound tuned config data and tuned profile YAML.
    :rtype: tuple[dict, str]
    """
    tuning_data: Dict = load_tuning(
        profile_defaults=load_profile_defaults(profile),
        tuning_files_list=tuning_files_list,
        tuning_data_list=tuning_data_list,
    )

    tuning_profile = get_profile_template(profile)
    tuning_data["profile_path"] = tuning_profile.name
    tuned_profile = tuning_profile.render(tuning_data)

    try:
        config_data = yaml.safe_load(tuned_profile)
    except yaml.YAMLError as exc:
        raise ProfileError('Unable to parse tuned profile "{}" {}'.format(profile, exc))

    return config_data, tuned_profile


def load_profile_defaults(profile: str) -> Dict:
    """Load default variables from a profile if available.

    Note:
        The profile will be rendered as scratch without any values
        to be able to be loaded as valid YAML.

    :param profile: Profile name (from package or from the user).
    :type profile: str

    :return: Default values mapping, if not available then an empty dict.
    :rtype: dict
    """
    # Scratch render of the profile template for _defaults extraction
    scratch_profile: Template = get_profile_template(profile)
    scratch_profile_rendered: str = scratch_profile.render()
    tmp_data = yaml.safe_load(scratch_profile_rendered)
    tuning_data = tmp_data.get("_defaults", {})
    LOG.debug("Tuning data: {}".format(tuning_data))
    return tuning_data


def get_profile_template(profile_name: str) -> Template:
    """Get a Jinja2 template via the environment generated for the selected profile
    (for fine-tuning of the profile).

    :param profile_name: Name of the template set
        (alternatively path to user-specified template set).
    :type profile_name: str

    :return: Jinja2 profile template for fine-tuning template.
    :rtype: Environment
    """
    LOG.debug(f"Profile name: {profile_name}")

    selected_template_name, selected_template_path = select_profile_file(profile_name)

    if not os.path.isdir(selected_template_path):
        raise TemplateError(
            'Unable to load requested profile location "%s"' % profile_name
        )

    loader = FileSystemLoader([selected_template_path, *get_profiles_paths()])

    extensions = ["jinja2_ansible_filters.AnsibleCoreFiltersExtension"]

    LOG.debug(f"Selected profile path: {selected_template_path}")

    try:
        env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=extensions,
        )
        template = env.get_template(selected_template_name)
    except Exception as e:
        LOG.exception("Error creating the Jinja2 environment.")
        raise TemplateError(
            "There was a problem with the templating environment."
        ) from e
    return template
