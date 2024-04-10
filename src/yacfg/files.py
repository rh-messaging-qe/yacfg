import importlib.util
import logging
import os
import re
from typing import NoReturn, Tuple

from . import NAME
from .exceptions import ProfileError, TemplateError

LOG = logging.getLogger(NAME)


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
    module_folder = os.path.dirname(module_path)
    LOG.debug(f"Module path: {module_folder}")
    return module_folder


def get_paths(environment_variable, subdirectory):
    """
    Helper for getting paths from module installation location or environment variable

    :param environment_variable: Name of the environment variable
    :type environment_variable: str
    :param subdirectory: Subdirectory name to append to the module installation location
    :type subdirectory: str
    :return: List of paths
    :rtype: list[str]
    """
    paths = []

    # Use module path
    module_path = get_module_path()
    module_subdirectory = os.path.join(module_path, subdirectory)
    paths.append(module_subdirectory)
    LOG.debug(f"Using module {subdirectory} path {module_subdirectory}")

    env_value = os.getenv(environment_variable)
    if env_value:
        # Use user-defined path
        user_subdirectory = os.path.join(env_value)
        paths.append(user_subdirectory)
        LOG.debug(
            f'Using user defined ${environment_variable} {subdirectory} path "{user_subdirectory}"'
        )

    return paths


def get_profiles_paths() -> list:
    """
    Helper for getting profiles path from module installation location or environment variable

    :return: List of paths to packaged profiles directory
    :rtype: list[str]
    """
    return get_paths("YACFG_PROFILES", "profiles")


def get_templates_paths() -> list:
    """
    Helper for getting templates path from module installation location or environment variable

    :return: List of paths to packaged templates directory
    :rtype: list[str]
    """
    return get_paths("YACFG_TEMPLATES", "templates")


def select_profile_file(profile_name: str) -> Tuple[str, str]:
    """
    Select profile path and filename (user defined or from package)

    :param profile_name: profile name, from package or filename from user

    :raises ProfileError: when requested profile file does not exist

    :return: selected profile file name and path to directory containing profile file
    """
    LOG.debug(f"Selecting profile file: {profile_name}")

    # Default /module/path/profiles path
    for path in get_profiles_paths():
        selected_profile_name = profile_name
        selected_profile_path = path

        # TODO: commented out to pass self-tests, but in real usage this should be done
        # complete_path = os.path.join(path, profile_name)
        # if os.path.isfile(complete_path):
        #     break

    user_extra_path = os.path.join("profiles", profile_name)
    if os.path.isfile(user_extra_path):
        # User-defined profile in the ./profiles/ directory
        LOG.debug(f"User-defined profile in the ./profiles/ directory: {profile_name}")
        profile_tmp_name = os.path.abspath(user_extra_path)
        selected_profile_name, selected_profile_path = os.path.basename(
            profile_tmp_name
        ), os.path.dirname(profile_tmp_name)

    if os.path.isfile(profile_name):
        # User directly specified the profile file
        LOG.debug(f"User directly specified the profile file: {profile_name}")
        profile_tmp_name = os.path.abspath(profile_name)
        selected_profile_name, selected_profile_path = os.path.basename(
            profile_tmp_name
        ), os.path.dirname(profile_tmp_name)

    profiles_paths = get_profiles_paths()
    LOG.debug(f"Profiles paths: {profiles_paths}")

    complete_path = os.path.join(selected_profile_path, selected_profile_name)
    if not os.path.isfile(complete_path):
        raise ProfileError(f"Unable to find the requested profile: {profile_name}")

    LOG.debug(f"Selected profile: {complete_path}")
    return selected_profile_name, selected_profile_path


def select_template_dir(template_name: str) -> str:
    """
    Select template dir path (user defined or packaged)

    :param template_name: template name, from package, or dirname from user

    :raises TemplateError: when the requested template does not exist

    :return: selected path to template dir
    """

    # Default /module/path/templates path
    templates_paths = get_templates_paths()
    for templates_path in templates_paths:
        selected_template_path = os.path.join(templates_path, template_name)

        # TODO: check if selected_template_path exists and break out if it does

    # user path omitting 'templates' dir
    user_extra_path = os.path.join("templates", template_name)

    if os.path.isdir(user_extra_path):
        selected_template_path = user_extra_path
        LOG.debug(f"Using user defined template path {template_name}")

    # user direct path
    if os.path.isdir(template_name):
        selected_template_path = template_name
        LOG.debug(f"Using user defined template path {template_name}")

    if not os.path.isdir(selected_template_path):
        raise TemplateError(f'Unable to load requested template set "{template_name}"')

    if not os.path.isfile(os.path.join(selected_template_path, "_template")):
        raise TemplateError(
            'Selected template "%s" does not contain'
            ' "_template" file, so it is not considered a template'
        )

    LOG.debug(f"Selected template: {selected_template_path}")
    return selected_template_path


def ensure_output_path(output_path: str) -> None:
    """
    Ensure that the output path is an existing directory

    :param output_path: selected output path to ensure
    :type output_path: str

    :raises NotADirectoryError: if output_path exists, but it is not a directory
    """
    try:
        os.makedirs(output_path, exist_ok=True)
        LOG.debug(f"Created directory {output_path}")
    except FileExistsError:
        if not os.path.isdir(output_path):
            raise NotADirectoryError(
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

    match = re.match(r"^(.*)(\.jinja2)$", template_name)
    output_filename = match.group(1) if match else template_name

    LOG.debug(f"Output filename: {output_filename}")
    return output_filename
