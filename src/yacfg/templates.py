import logging

from jinja2 import ChoiceLoader, Environment, FileSystemLoader

from . import NAME
from .exceptions import TemplateError
from .files import get_templates_paths, select_template_dir

LOG: logging.Logger = logging.getLogger(NAME)


def get_template_environment(template_name):
    """Create Jinja2 environment for the selected template.

    :param template_name: Name of the template set or path to a user-specified template set.
    :type template_name: str

    :return: Jinja2 environment.
    :rtype: Environment

    :raises TemplateError: If there is a problem with the templating environment.
    """
    LOG.debug(f"Template name: {template_name}")

    selected_template_path = select_template_dir(template_name)
    LOG.debug(f"Selected template path: {selected_template_path}")

    loader = ChoiceLoader(
        [
            FileSystemLoader(selected_template_path),
            FileSystemLoader(get_templates_paths()),
        ]
    )
    extensions = ["jinja2_ansible_filters.AnsibleCoreFiltersExtension"]

    try:
        env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=extensions
        )
    except Exception as e:
        LOG.exception("Error creating the Jinja2 environment.")
        raise TemplateError(
            "There was a problem with the templating environment."
        ) from e

    return env
