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
import daiquiri
import time

from bter.http import http_util

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


class BterBtcPollster(object):
    def __init__(self, conf=None):
        self.conf = conf
        self.http_client = http_util.HttpClient()

    def get_samples(self):
        logger.debug("In the plugin:%s" % "BterBtcPollster")
        timestamp = time.strftime("%Y-%m-%d %X", time.localtime())

        logger.info("all the target url is:%s" % TARGET_URLS)
        for item in TARGET_URLS:
            if item.get('name') in SUPPORT_NAME:
                sample = {'counter_name': item.get('name'),
                          'timestamp': timestamp,
                          'volume': 0,
                          'resource_metadata': {}}
                try:
                    response = self.http_client.download(item.get('url'))
                    logger.debug("get the data is:%s" % response.content)
                    if response.status_code == 200:
                        sample['resource_metadata'] = response.content
                except Exception as err:
                    logger.error("get data failed item:%s error:%s" %
                                 (item, err))

                yield sample
