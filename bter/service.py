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

import ConfigParser
import daiquiri
import daiquiri.formatter
import logging
import os
import sys


def service_prepare(argv=None, config_file=None, conf=None):
    if argv is None:
        argv = sys.argv
    if conf is None:
        conf = ConfigParser.ConfigParser()

    if config_file is None or not os.path.exists(config_file):
        raise Exception("The config file [%s] is not exists or "
                        "is None." % config_file)
    conf.read(config_file)

    conf_path, conf_file = os.path.split(config_file)
    conf.set("DEFAULT", "conf_path", conf_path)
    conf.set('DEFAULT', 'conf_file', conf_file)

    init_log_info(conf=conf)
    return conf


LOG_LEVEL = {
    'INFO': logging.INFO,
    'WARN': logging.WARNING,
    'ERROR': logging.ERROR,
    'DEBUG': logging.DEBUG
}


def init_log_info(conf=None):
    if conf is None:
        raise Exception("Need conf object")
    log_path = conf.get('log', 'log_path')
    log_filename = conf.get('log', 'log_filename')
    log_level_name = conf.get('log', 'log_level').upper()
    log_level = LOG_LEVEL.get(log_level_name, logging.INFO)
    log_format = conf.get('log', 'log_format', raw=True)

    if not os.path.isdir(log_path):
        os.mkdir(log_path)
    log_file = log_path + "/" + log_filename
    daiquiri.setup(
        level=log_level,
        outputs=(
            daiquiri.output.Stream(formatter=daiquiri.formatter.ColorFormatter(
                fmt=log_format)),
            daiquiri.output.File(log_file,
                                 formatter=daiquiri.formatter.ColorFormatter(
                                     fmt=log_format)),
        )
    )
