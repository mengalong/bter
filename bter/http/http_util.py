# encoding:utf8

import requests


class HttpClient(object):
    def __init__(self):
        pass

    def download(self, url):
        try:
            response = requests.get(url, timeout=3)
        except Exception as err:
            raise err
        return response
