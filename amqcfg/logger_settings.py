# Copyright 2018 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys

FORMAT_CONSOLE = '[%(asctime)s] [%(levelname)s] %(name)s :: %(message)s'
FORMAT_CONSOLE_COLOR = '[%(asctime)s] [%(log_color)s%(levelname)s%(reset)s]' \
                       ' %(name)s :: %(message)s'

DATE_FORMAT_ISO = '%Y-%m-%d %H:%M:%S,'
DATE_FORMAT_TIME = '%H:%M:%S'


def config_console_logger(filename=None, level=None, fmt=None, fmt_color=None,
                          datefmt=None):
    """ configure console logger, if colorlog is installed it will use colorlog
    :param filename: stream to log into, default sys.stdout
    :param level: console log level
    :param fmt: console log format
    :param fmt_color: console color log format (only with colorlog)
    :param datefmt: formatter date format, default like ISO8601
    """
    import_error_msg = []
    # Windows compatibility section for colorama
    try:
        # noinspection PyUnresolvedReferences
        import colorama
        colorama.init()
    except ImportError:
        try:
            # noinspection PyUnresolvedReferences
            import colorlog
        except ImportError:
            import platform
            if platform.system() == 'Windows':
                import_error_msg.append(
                    'Colorlog without colorama used, expect escape codes,'
                    ' please install colorama'
                )

    filename = filename or sys.stdout
    level = level or logging.DEBUG
    fmt = fmt or FORMAT_CONSOLE
    fmt_color = fmt_color or FORMAT_CONSOLE_COLOR
    datefmt = datefmt or DATE_FORMAT_TIME

    # console handler
    # console_handler = logging.StreamHandler(stream=filename)  # Python 2.7
    console_handler = logging.StreamHandler()  # Python 2.6
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(fmt, datefmt=datefmt)

    try:
        # noinspection PyUnresolvedReferences
        import colorlog  # noqa: F811
        console_formatter = colorlog.ColoredFormatter(
            fmt_color,
            log_colors={
                'CRITICAL': 'black,bg_red',
                'ERROR': 'red',
                'WARNING': 'yellow',
                'SKIP': 'blue',
                'FAIL': 'bold_red',
                'PASS': 'bold_green',
                'INFO': 'reset',
                'DOC': 'purple',
                'DEBUG': 'cyan',
            },
            datefmt=datefmt,
        )
    except ImportError:
        # import_error_msg.append(
        #     "cannot initialize colorlog, using boring streamhandler"
        # )
        pass
    console_handler.setFormatter(console_formatter)
    logging.getLogger().addHandler(console_handler)
    # log all above error messages
    if import_error_msg:
        for log_err in import_error_msg:
            logging.info(log_err)


# default logger level INFO
logging.getLogger().setLevel(logging.INFO)
