try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore

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
