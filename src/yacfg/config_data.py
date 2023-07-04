import datetime
import time
from collections import namedtuple
from typing import Dict

from . import NAME, __version__

RenderOptions = namedtuple("RenderOptions", ["generator_notice", "licenses"])


def add_template_metadata(config_data: Dict) -> None:
    """Add templating metadata to the original template data.

    :param config_data: Original template data.
    :type config_data: dict
    """
    now = datetime.datetime.now()
    date_format = "%Y-%m-%d"
    time_format = "%H:%M"

    config_data["metadata"] = {
        "tool_name": NAME,
        "tool_version": __version__,
        "datetime": {
            "datetime": now.strftime(f"{date_format} {time_format}"),
            "year": now.strftime("%Y"),
            "time": now.strftime(time_format),
            "date": now.strftime(date_format),
            "unix": time.time(),
        },
    }


def add_render_config(config_data: Dict, render_options: "RenderOptions") -> None:
    """Add render-related config to the original template data.

    :param config_data: Original template data.
    :type config_data: dict
    :param render_options: Render options to tune up rendering.
    :type render_options: RenderOptions
    """
    render_config = {
        "generator_notice": render_options.generator_notice,
        "licenses": render_options.licenses,
    }

    config_data.setdefault("render", {}).update(render_config)
