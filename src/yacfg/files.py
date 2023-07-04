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
    :type profile_name: str

    :raises ProfileError: when requested profile file does not exist

    :return: selected path to profile and profile name
    :rtype: tuple[str, str]
    """
    LOG.debug(f"Selecting profile file: {profile_name}")

    user_extra_path = os.path.join("profiles", profile_name)
    if os.path.isfile(user_extra_path):
        # User-defined profile in the ./profiles/ directory
        LOG.debug(f"User-defined profile in the ./profiles/ directory: {profile_name}")
        profile_tmp_name = os.path.abspath(user_extra_path)
        return profile_name, os.path.dirname(profile_tmp_name)

    if os.path.isfile(profile_name):
        # User directly specified the profile file
        LOG.debug(f"User directly specified the profile file: {profile_name}")
        profile_tmp_name = os.path.abspath(profile_name)
        return profile_name, os.path.dirname(profile_tmp_name)

    profiles_paths = get_profiles_paths()
    LOG.debug(f"Profiles paths: {profiles_paths}")

    for path in profiles_paths:
        complete_path = os.path.join(path, profile_name)
        if os.path.isfile(complete_path):
            LOG.debug(f"Selected profile: {complete_path}")
            return profile_name, complete_path

    raise ProfileError(f"Unable to find the requested profile: {profile_name}")


def select_template_dir(template_name: str) -> str:
    """
    Select template dir path (user defined or packaged)

    :param template_name: template name, from package, or dirname from user
    :type template_name: str

    :raises TemplateError: when the requested template does not exist

    :return: selected path to template dir
    :rtype: str
    """

    templates_paths = get_templates_paths()
    LOG.debug(f"Templates path: {templates_paths}")

    user_extra_path = os.path.join("templates", template_name)

    if os.path.isdir(user_extra_path) or os.path.isdir(template_name):
        # User-defined template path without the "templates" directory or directly specified template directory
        selected_template_path = (
            user_extra_path if os.path.isdir(user_extra_path) else template_name
        )
        LOG.debug(f"Using user-defined template path {selected_template_path}")

    else:
        selected_template_path = next(
            (
                os.path.join(template_path, template_name)
                for template_path in templates_paths
                if os.path.isdir(os.path.join(template_path, template_name))
                and os.path.isfile(
                    os.path.join(template_path, template_name, "_template")
                )
            ),
            None,
        )

        if selected_template_path is None:
            raise TemplateError(
                f"Unable to load the requested template set: {template_name}"
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
