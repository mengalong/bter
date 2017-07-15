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

import cotyledon
import ConfigParser
import daiquiri
import sys

from bter.agent import manager
from bter.http import http_util
from bter import service


logger = daiquiri.getLogger(__name__)


TARGET_URLS = [
    {
        "name": "get_all_pairs",
        "url": "http://data.bter.com/api2/1/pairs"
    },
    {
        "name": "get_market_info",
        "url": "http://data.bter.com/api2/1/marketinfo"
    },
    {
        "name": "get_tickers",
        "url": "http://data.bter.com/api2/1/tickers"
    },
    {
        "name": "get_btc_cny",
        "url": "http://data.bter.com/api2/1/ticker/btc_cny"
    }
]

SUPPORT_NAME = ['get_btc_cny']


class Manager(object):
    def __init__(self, urls, conf=None):
        self.conf = conf
        self.http_client = http_util.HttpClient()
        self.target_urls = urls

    def _get_data(self, url=None):
        if url is None:
            logger.error("The url is None ignore it")
            return None

        response = self.http_client.download(url)
        return response

    def get_datas(self):
        for url_item in self.target_urls:
            # import pdb;pdb.set_trace()
            url_name = url_item.get('name')
            if url_name in SUPPORT_NAME:
                url_target = url_item.get('url')
                response = self._get_data(url=url_target)
                if response is not None:
                    logger.info("Fetch the api name:%s url:%s data:%s" %
                                (url_name, url_target, response.content))


# if __name__ == "__main__":
#     manager = Manager(TARGET_URLS)
#     manager.get_datas()

def create_agent(work_id, conf):
    namespaces = conf.get('DEFAULT', 'namespaces').split(',')
    return manager.AgentManager(conf, namespaces)

def main():
    conf = ConfigParser.ConfigParser()
    service.service_prepare(config_file=sys.argv[1], conf=conf)
    logger.info("The config path is:%s" % conf.get('DEFAULT', 'conf_path'))
    logger.error("The error log")
    sm = cotyledon.ServiceManager()
    sm.add(create_agent, args=(conf,))
    sm.run()

if __name__ == "__main__":
    main()
