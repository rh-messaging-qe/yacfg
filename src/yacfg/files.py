import logging
import os
import re
from typing import Tuple, NoReturn
import importlib.util

from .exceptions import ProfileError, TemplateError
from .meta import NAME

LOG = logging.getLogger(NAME)

REX_TEMPLATE_TO_OUTPUT = re.compile(r"^(.*)(\.jinja2)$")


def get_module_path() -> str:
    """
    Get module installation path,
    for reading packaged template sets and profiles

    :return: module installation path
    :rtype: str

    :raises ModuleNotFoundError: when module path is not found
    """
    module_spec = importlib.util.find_spec(__name__)
    if module_spec is None or module_spec.origin is None:
        raise ModuleNotFoundError("Module path not found")

    module_path = module_spec.origin
    LOG.debug(f"Module path: {module_path}")
    return module_path


def get_profiles_path() -> str:
    """
    Helper for getting profiles path from module installation location

    :return: path to packaged profiles directory
    :rtype: str
    """
    env_profiles = os.getenv("YACFG_PROFILES")

    if env_profiles:
        # Use user-defined profiles path
        profiles_path = os.path.join(env_profiles)
        LOG.debug(f"Using user defined $YACFG_PROFILES profiles path {profiles_path}")
    else:
        # Use module profiles path
        module_path = get_module_path()
        profiles_path = os.path.join(module_path, "profiles")
        LOG.debug(f"Using module profiles path {profiles_path}")

    return profiles_path


def get_templates_path() -> str:
    """
    Helper for getting templates path from module installation location

    :return: path packaged templates directory
    :rtype: str
    """
    env_templates = os.getenv("YACFG_TEMPLATES")

    if env_templates:
        # Use user-defined templates path
        templates_path = os.path.join(env_templates)
        LOG.debug(
            f'Using user defined $YACFG_TEMPLATES template path "{templates_path}"'
        )
    else:
        # Use module templates path
        module_path = get_module_path()
        templates_path = os.path.join(module_path, "templates")
        LOG.debug(f"Using module templates path {templates_path}")

    return templates_path


def select_profile_file(profile_name: str) -> Tuple[str, str]:
    """
    Select profile path and filename (user defined or from package)

    :param profile_name: profile name, from package or filename from user
    :type profile_name: str

    :raises ProfileError: when requested profile file does not exist

    :return: selected path to profile and profile name
    :rtype: tuple[str, str]
    """
    LOG.debug(f"Selecting profile file: {profile_name}")

    profiles_path = get_profiles_path()
    LOG.debug(f"Profiles path: {profiles_path}")

    selected_profile_path = profiles_path
    selected_profile_name = profile_name

    user_extra_path = os.path.join("profiles", profile_name)

    if os.path.isfile(user_extra_path):
        # User-defined profile in the ./profiles/ directory
        LOG.debug(f"User ./profile/ omitting profile {profile_name}")
        profile_tmp_name = os.path.abspath(user_extra_path)
        selected_profile_path = os.path.dirname(profile_tmp_name)
        selected_profile_name = os.path.basename(profile_tmp_name)

    elif os.path.isfile(profile_name):
        # User directly specified the profile file
        LOG.debug(f"User direct profile {profile_name}")
        profile_tmp_name = os.path.abspath(profile_name)
        selected_profile_path = os.path.dirname(profile_tmp_name)
        selected_profile_name = os.path.basename(profile_tmp_name)

    complete_path = os.path.join(selected_profile_path, selected_profile_name)

    if not os.path.isfile(complete_path):
        raise ProfileError(f"Unable to find the requested profile: {profile_name}")

    LOG.debug(f"Selected profile: {complete_path}")
    return selected_profile_name, selected_profile_path


def select_template_dir(template_name: str) -> str:
    """
    Select template dir path (user defined or packaged)

    :param template_name: template name, from package, or dirname from user
    :type template_name: str

    :raises TemplateError: when the requested template does not exist

    :return: selected path to template dir
    :rtype: str
    """

    templates_path = get_templates_path()
    LOG.debug(f"Templates path: {templates_path}")

    selected_template_path = os.path.join(templates_path, template_name)

    user_extra_path = os.path.join("templates", template_name)

    if os.path.isdir(user_extra_path):
        # User-defined template path without the "templates" directory
        selected_template_path = user_extra_path
        LOG.debug(f"Using user defined template path {template_name}")

    elif os.path.isdir(template_name):
        # User directly specified the template directory
        selected_template_path = template_name
        LOG.debug(f"Using user defined template path {template_name}")

    if not os.path.isdir(selected_template_path):
        raise TemplateError(
            f"Unable to load the requested template set: {template_name}"
        )

    if not os.path.isfile(os.path.join(selected_template_path, "_template")):
        raise TemplateError(
            f'Selected template "{template_name}" does not contain '
            f'"_template" file, so it is not considered a template'
        )

    LOG.debug(f"Selected template: {selected_template_path}")
    return selected_template_path


def ensure_output_path(output_path: str) -> NoReturn:
    """
    Ensure that the output path is an existing directory

    :param output_path: selected output path to ensure
    :type output_path: str

    :raises OSError: if output_path exists, but it is not a directory
    """
    LOG.debug(f"Ensuring output path: {output_path}")

    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
        LOG.debug(f"Created directory {output_path}")
    elif not os.path.isdir(output_path):
        raise OSError(
            f'Output path "{output_path}" already exists and it is not a directory!'
        )
    else:
        LOG.debug(f"Requested directory {output_path} exists")


def get_output_filename(template_name: str) -> str:
    """
    Process a template filename and get the output file name

    .. note: removing '.jinja2' suffix

    :param template_name: filename of a template
    :type template_name: str

    :return: output filename based on the template name
    :rtype: str
    """
    LOG.debug(f"Getting output filename: {template_name}")

    match = REX_TEMPLATE_TO_OUTPUT.match(template_name)
    output_filename = template_name
    if match:
        output_filename = match.group(1)

    LOG.debug(f"Output filename: {output_filename}")
    return output_filename
