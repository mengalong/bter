# coding=utf8
#  Copyright 2017~ mengalong <alongmeng@gmail.com>
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

from bter.agent import manager
from bter import service


if __name__ == "__main__":
    conf = ConfigParser.ConfigParser()
    config_file = "/Users/mengalong/code/git/bter/etc/bter/bter.ini"
    service.service_prepare(config_file=config_file, conf=conf)

    namespaces = conf.get('DEFAULT', 'namespaces').split(',')
    manager = manager.AgentManager(conf, namespaces)
    for item in manager.extensions:
        print("get the extension:%s" % item.name)
        print(item.obj.get_samples())

    print(manager.polling_manager.sources)
    manager.run()
