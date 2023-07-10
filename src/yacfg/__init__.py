import sys

if sys.version_info < (3, 10):
    # compatibility for python <3.10
    import importlib_metadata as metadata
else:
    from importlib import metadata

try:
    __version__ = metadata.version("yacfg")
except metadata.PackageNotFoundError:
    __version__ = "devel"

NAME = "yacfg"
SHORT_DESCRIPTION = "Template based configuration generator"
DESCRIPTION = (
    "Template based configuration files generator based on jinja2 and yaml"
    " mainly focused on Apache ActiveMQ Artemis and related projects"
)
