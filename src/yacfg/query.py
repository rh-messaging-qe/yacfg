import logging
import os
import posixpath
import re
from typing import List

from jinja2.environment import Environment

from .files import NAME, get_profiles_paths, get_templates_paths

LOG: logging.Logger = logging.getLogger(NAME)


def filter_template_list(
    template_list: List[str], output_filter: List[str]
) -> List[str]:
    """Filter templates based on output filter regular expressions.

    :param template_list: List of template file names.
    :type template_list: list[str]
    :param output_filter: List of regular expressions to filter out templates.
    :type output_filter: list[str]
    :return: List of selected template file names to process.
    :rtype: list[str]
    """
    filtered_templates = [
        template
        for template in template_list
        if any(re.match(flt, template) for flt in output_filter)
    ]
    LOG.debug(f"Filtered template files list: {filtered_templates}")
    return filtered_templates


def list_templates() -> List[str]:
    """List all packaged templates with their package relative path.

    Package is a directory under 'templates' directory that contains
    a file named '_template'. It would be good if the template directory
    contains some Jinja2 templates.

    :return: List of template paths from the package.
    :rtype: list[str]
    """
    templates_paths: list = get_templates_paths()
    LOG.debug(f"Templates path for query: {templates_paths}")

    template_paths = []
    for template in templates_paths:
        for root, dirs, files in os.walk(template):
            if any(file.endswith((".yaml", ".jinja2", ".j2")) for file in files):
                if "_template" in files:
                    relative_path = os.path.relpath(root, template)
                    template_path = posixpath.join(*relative_path.split(os.path.sep))
                    template_paths.append(template_path)
                    LOG.debug(
                        f"Included template path: {template_path} (using _template)"
                    )
                else:
                    LOG.debug(f"Template files found, but no _template file in {root}")

    LOG.debug(f"Template paths: {template_paths}")
    return template_paths


def list_profiles() -> List[str]:
    """List all packaged complete profiles with their package relative path.

    Profile is any YAML file under the 'profiles' directory in the package
    that is not placed under a directory with a leading underscore like '_modules'.

    :return: List of profiles from the package.
    :rtype: list[str]
    """
    profiles_paths = get_profiles_paths()
    LOG.debug(f"Profiles path for query: {profiles_paths}")

    profile_paths = []

    for profiles in profiles_paths:
        for root, dirs, files in os.walk(profiles):
            dirs[:] = [d for d in dirs if not d.startswith("_")]
            for file in files:
                if file.endswith((".yaml", ".jinja2", ".j2")):
                    relative_path = os.path.relpath(os.path.join(root, file), profiles)
                    profile_paths.append(
                        posixpath.join(*relative_path.split(os.path.sep))
                    )

    LOG.debug(f"Profile paths: {profile_paths}")
    return profile_paths


def get_main_template_list(env: Environment) -> List[str]:
    """Get a list of main templates from the selected template set.

    Note:
        Main template -> template that resembles an output config file.

    :param env: Jinja2 environment.
    :type env: Environment
    :return: List of main template names.
    :rtype: list[str]
    """
    main_template_regex = re.compile(r"^[^/]+\.jinja2$")
    main_template_list = env.list_templates(filter_func=main_template_regex.match)
    LOG.debug(f"Main template files list: {main_template_list}")
    return main_template_list
