import boto3
from Queue import Queue
import time
import threading
import gevent

class DynamoStreamClient(threading.Thread):
    def __init__(self, queue_list, old_items, arn):
        self.queue_list = queue_list
        self.old_items = old_items
        self.arn = arn
        self.queue = Queue()
        self.should_stop = False
        super(DynamoStreamClient, self).__init__()

    def run(self):
        self.client = boto3.client('dynamodbstreams')
        while(True and not self.should_stop):
            print('getting new shard')
            latest_shard = self.get_latest_shard()
            latest_iterator = self.get_latest_shard_iterator(
                    latest_shard['ShardId'])
            shard_iterator = latest_iterator['ShardIterator']
            self.iterate_shard(shard_iterator)
            if not self.should_stop:
                gevent.sleep(1)

    def stop(self):
        self.should_stop = True

    def iterate_shard(self, shard_iterator):
        print('iterating shard')
        while(shard_iterator and not self.should_stop):
            records_response = self.get_records(shard_iterator)
            records = records_response['Records']
            for record in records:
                data = record['dynamodb']['NewImage']
                msg = {}
                if self.arn.find('temp_history') > -1:
                    ts = int(data['timestamp'].values()[0])
                    temp = float(data['temperature'].values()[0])
                    msg['type'] = 'temp_hist'
                    msg['timestamp'] = ts
                    msg['temperature'] = temp
                    print(str(ts) + ' ' + str(temp))
                elif self.arn.find('miscellaneous') > -1:
                    print(data)
                    key = data.get('any_key').values()[0]
                    if key == 'min_temp':
                        msg['type'] = key
                        msg['temperature'] = int(data['temp'].values()[0])
                    elif key == 'max_temp':
                        msg['type'] = key
                        msg['temperature'] = int(data['temp'].values()[0])
                    else:
                        print('oh no!')
                else:
                    msg['type'] = 'unknown'
                    msg['data'] = data
                self.fill_queues(msg)
            if len(records) == 0:
                gevent.sleep(1)
            shard_iterator = records_response.get('NextShardIterator')

    def fill_queues(self, item):
        self.old_items.append(item)
        if len(self.old_items) > 1000:
            self.old_items.pop(0)
        for queue in self.queue_list:
            queue.put(item)

    @staticmethod
    def get_start_seq(shard):
        return int(shard['SequenceNumberRange']['StartingSequenceNumber'])

    def get_latest_shard(self):
        response = self.client.describe_stream(StreamArn=self.arn, Limit=100)
        shards = response['StreamDescription']['Shards']
        latest_shard = shards[0]
        latest_start_seq = DynamoStreamClient.get_start_seq(latest_shard)
        for shard in shards:
            cur_start_seq = DynamoStreamClient.get_start_seq(shard)
            if cur_start_seq > latest_start_seq:
                latest_shard = shard
                latest_start_seq = cur_start_seq
        return latest_shard

    def get_latest_shard_iterator(self, shardId):
        return self.client.get_shard_iterator(
            StreamArn=self.arn,
            ShardId=shardId,
            ShardIteratorType='LATEST'
        )

    def get_records(self, shard_iterator):
        return self.client.get_records(
            ShardIterator=shard_iterator,
            Limit=100
        )

