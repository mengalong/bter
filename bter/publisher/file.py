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
import logging
import logging.handlers

from six.moves.urllib import parse as urlparse

logger = daiquiri.getLogger(__name__)


class FilePublisher(object):
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

        logger.debug("The parsed url is:%s" % str(parsed_url))

        params = urlparse.parse_qs(parsed_url.query)
        max_bytes = int(params.get('max_bytes')[0])
        backup_count = int(params.get('backup_count')[0])
        logger.debug("max_bytes:%d backup_count:%d" %
                     (max_bytes, backup_count))

        # create rotating file handler
        rfh = logging.handlers.RotatingFileHandler(
            parsed_url.path, encoding='utf8', maxBytes=max_bytes,
            backupCount=backup_count)

        self.publisher_logger = logging.Logger('publisher.file')
        self.publisher_logger.propagate = False
        self.publisher_logger.setLevel(logging.INFO)
        rfh.setLevel(logging.INFO)
        self.publisher_logger.addHandler(rfh)

    def record_metering_sample(self, sample):
        self.publisher_logger.info(sample)
