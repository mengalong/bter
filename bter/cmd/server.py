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
import cotyledon
import daiquiri
import sys


from bter.agent import manager
from bter import service


logger = daiquiri.getLogger(__name__)


def create_agent(work_id, conf):
    namespaces = conf.get('DEFAULT', 'namespaces').split(',')
    return manager.AgentManager(conf, namespaces)


def main():
    conf = ConfigParser.ConfigParser()
    service.service_prepare(config_file=sys.argv[1], conf=conf)
    logger.info("The config path is:%s" % conf.get('DEFAULT', 'conf_path'))
    sm = cotyledon.ServiceManager()
    sm.add(create_agent, args=(conf,))
    sm.run()

if __name__ == "__main__":
    main()
