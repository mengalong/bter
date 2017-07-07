# coding: utf-8

import daiquiri
import daiquiri.formatter
import sys

from bter.http import http_util
from bter import utils

log_path = sys.path[0] + "/../log"
log_file = "bter.log"
utils.init_log_info(log_path, log_file)
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


if __name__ == "__main__":
    manager = Manager(TARGET_URLS)
    manager.get_datas()
