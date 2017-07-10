# Copyright 2017~ mengalong <alongmeng@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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
