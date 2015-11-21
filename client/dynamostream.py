import boto3
from Queue import Queue
import time
import threading
import gevent

class DynamoStreamClient(threading.Thread):
    def __init__(self):
        self.arn = 'arn:aws:dynamodb:us-west-2:630535199163:table/temp_history/stream/2015-11-21T12:12:53.316'
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

    def get_queue(self):
        return self.queue

    def iterate_shard(self, shard_iterator):
        print('iterating shard')
        while(shard_iterator and not self.should_stop):
            records_response = self.get_records(shard_iterator)
            records = records_response['Records']
            for record in records:
                data = record['dynamodb']['NewImage']
                ts = int(data['timestamp'].values()[0])
                temp = float(data['temperature'].values()[0])
                self.queue.put({'timestamp': ts, 'temperature': temp})
                print(str(ts) + ' ' + str(temp))
            if len(records) == 0:
                gevent.sleep(1)
            shard_iterator = records_response.get('NextShardIterator')

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

