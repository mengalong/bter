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

import MySQLdb

from six.moves.urllib import parse as urlparse


class MysqlClient(object):
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = db

        self.init_connection_handler()

    def init_connection_handler(self):
        conn = MySQLdb.connect(host='localhost',
                               port=3306,
                               user='root',
                               passwd='123456',
                               db='bter')
        cur = conn.cursor()
        self.conn = conn
        self.cur = cur

    def insert(self, cmd):
        result = self.cur.execute(cmd)
        self.conn.commit()
        return result

    def select(self, cmd):
        result = self.cur.execute(cmd)
        return self.cur.fetchmany(result)


def test_insert_data(obj):
    data = {"result": "true", "last": 13905.63, "lowestAsk": 14086.25,
            "highestBid": 13905.83, "percentChange": -4.5729481196816,
            "baseVolume": 3524003.37, "quoteVolume": 251.6904,
            "high24hr": 14678.96, "low24hr": 13422.21}
    data_re = str(data)
    sql_cmd = "insert into meter (counter_name, timestamp, volume, " \
              "resource_metadata) values('bter_btc', " \
              "'2017-07-20:11:20:22', 0, \"%s\")" % data_re
    result = obj.insert(sql_cmd)
    print("test insert data result:%s" % result)


def test_select_data(obj):
    sql_cmd = "select * from meter"
    result = obj.select(sql_cmd)
    for i in result:
        print("test get data from db:%s" % str(i))


def test_parse_conn(obj):
    conn = "mysql://root:123456@localhost:3306/bter"

    # parsed_url = netutils.urlsplit(conn)
    parsed_url = urlparse.urlparse(conn)
    print(parsed_url.username)
    print(parsed_url.password)
    print(parsed_url.port)
    print(parsed_url.hostname)
    print(parsed_url)


def main():
    db_obj = MysqlClient('localhost', 3306, 'root', '123456', 'bter')

    # test_select_data(db_obj)
    test_parse_conn(db_obj)


if __name__ == "__main__":
    main()
