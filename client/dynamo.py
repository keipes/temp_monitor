import boto
from boto.dynamodb2.table import Table
from boto.dynamodb2.exceptions import ItemNotFound
import time
import util
import decimal
from boto.dynamodb.types import DYNAMODB_CONTEXT
# Inhibit Inexact Exceptions
DYNAMODB_CONTEXT.traps[decimal.Inexact] = 0
# Inhibit Rounded Exceptions
DYNAMODB_CONTEXT.traps[decimal.Rounded] = 0

class DynamoClient():
    def __init__(self):
        self.conn = boto.dynamodb2.connect_to_region('us-west-2')
        print(self.conn.list_tables())
        if util.is_dev_environment():
            table = 'temp_history_dev'
        else:
            table = 'temp_history'
        self.temp_hist = Table(table, connection=self.conn)


    def record_temperature(self, temp):
        print(DynamoClient.get_timestamp())
        self.temp_hist.put_item(data={
            'timestamp': DynamoClient.get_timestamp(),
            'temperature': temp
        })

    def get_latest_temperature(self, max_history=6000):
        ts = DynamoClient.get_timestamp()
        for t in xrange(ts, ts - max_history, -1):
            print(t)
            try:
                return self.temp_hist.get_item(timestamp=t)
            except ItemNotFound:
                pass

    @staticmethod
    def get_timestamp():
        return int(time.mktime(time.gmtime()) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0)))

