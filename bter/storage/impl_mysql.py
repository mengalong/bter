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
import MySQLdb

logger = daiquiri.getLogger(__name__)


class MysqlClient(object):
    def __init__(self, parsed_url):
        # parsed_url = urlparse.urlparse(self.url)
        self.host = parsed_url.hostname
        self.port = parsed_url.port
        self.user = parsed_url.username
        self.passwd = parsed_url.password
        self.database = parsed_url.path.split('/')[1]

        self.init_connection_handler()

    def init_connection_handler(self):
        conn = MySQLdb.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.database,)
        cur = conn.cursor()
        self.conn = conn
        self.cur = cur

    def insert(self, sample):
        data = sample['resource_metadata']
        data_re = str(data)
        sql_cmd = "insert into meter (counter_name, timestamp, volume, " \
                  "resource_metadata) values(\"%s\", \"%s\", %d, \'%s\')" % \
                  (sample['counter_name'], sample['timestamp'],
                   sample['volume'], data_re)
        logger.debug("sql_cmd is:%s" % sql_cmd)
        result = self.cur.execute(sql_cmd)
        self.conn.commit()
        return result

    def select(self, cmd):
        result = self.cur.execute(cmd)
        return self.cur.fetchmany(result)
