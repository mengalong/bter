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
import os
import yaml

logger = daiquiri.getLogger(__name__)


class ConfigManagerBase(object):
    def __init__(self, conf):
        self.conf = conf
        self.cfg_loc = None

    def load_config(self, cfg_file):
        """Load a configuration file and set its refresh values."""
        if os.path.exists(cfg_file):
            self.cfg_loc = cfg_file

        with open(self.cfg_loc) as fap:
            data = fap.read()
        conf = yaml.safe_load(data)
        logger.info("Config file: %s", conf)
        return conf


class PipeLineManager(ConfigManagerBase):
    def __init__(self, conf, cfg_file):
        self.conf = conf
        cfg = self.load_config(cfg_file)

        unique_names = set()
        sources = []
        for s in cfg.get('sources'):
            name = s.get('name')
            if name in unique_names:
                # TODO(mengalong): use the pipelineException
                raise Exception("Duplicated source names: %s" % name)
            else:
                unique_names.add(name)
                sources.append(s)
        unique_names.clear()
        self.sources = sources
