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

from six.moves.urllib import parse as urlparse
from stevedore import driver

logger = daiquiri.getLogger(__name__)


class PublisherManager(object):
    def __init__(self, conf, url):
        self.conf = conf
        self.url = url

        parsed_url = urlparse.urlparse(url)
        logger.debug("The parsed url for publisher is :%s" % str(parsed_url))
        self.publish_driver = driver.DriverManager(
            'bter.publisher',
            parsed_url.scheme,
            invoke_args=(self.conf,),
            invoke_on_load=True).driver
