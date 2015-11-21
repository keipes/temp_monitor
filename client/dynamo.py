import boto
import time

class DynamoClient():
    def __init__(self):
        boto.connect_dynamodb()
        self.conn = boto.dynamodb.connect_to_region('us-west-2')
        self.temp_hist = self.conn.get_table('temp_history')

    def record_temperature(self, temp):
        print(DynamoClient.get_timestamp())
        item = self.temp_hist.new_item(
            hash_key = DynamoClient.get_timestamp(),
            attrs = {
                'temperature': temp
            }
        )
        item.put()

    @staticmethod
    def get_timestamp():
        return int(time.mktime(time.gmtime()) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0)))

