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


class DataBasePublisher(object):
    """Publisher metering data to file.

    The file publisher pushes metering data into a file. The file name and
    location should be configured in bter pipeline configuration file.
    If a file name and location is not specified, this File Publisher will not
    log any meters other than log a warning in bter log file.

    To enable this publisher, add the following section to the
    /etc/bter/pipeline.yaml file or simply add it to an existing
    pipeline::

        -
            name: meter_file
            interval: 600
            counters:
                - "*"
            transformers:
            publishers:
                - file:///var/test?max_bytes=10000000&backup_count=5

    File path is required for this publisher to work properly. If max_bytes
    or backup_count is missing, FileHandler will be used to save the metering
    data. If max_bytes and backup_count are present, RotatingFileHandler will
    be used to save the metering data.
    """

    def __init__(self, conf):
        self.conf = conf
        self.url = self.conf.get('database', 'connection')
        parsed_url = urlparse.urlparse(self.url)

        logger.debug("The database url is:%s" % self.url)
        d = driver.DriverManager(
            namespace="bter.storage",
            name=parsed_url.scheme,
            invoke_on_load=True,
            invoke_args=(parsed_url,)).driver

        self.database = d
        logger.debug("the database obj is:%s" % self.database)


    def record_metering_sample(self, sample):
        self.database.insert(sample)
