import daiquiri
import daiquiri.formatter
import logging
import os


def init_log_info(log_path, log_filename):
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
    log_file = log_path + "/" + log_filename
    daiquiri.setup(
        level=logging.INFO,
        outputs=(
            daiquiri.output.Stream(formatter=daiquiri.formatter.ColorFormatter(
                fmt="%(asctime)s [PID %(process)d] [%(levelname)s] "
                    "%(name)s:%(lineno)d %(message)s")),
            daiquiri.output.File(log_file,
                                 formatter=daiquiri.formatter.ColorFormatter(
                                     fmt="%(asctime)s [PID %(process)d] "
                                         "[%(levelname)s] %(name)s:%(lineno)d "
                                         "%(message)s")),
        )
    )
