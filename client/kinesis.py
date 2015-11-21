import boto



class KinesisClient():
    def __init__(self):
        boto.connect_kinesis()
        self.kinesis = boto.kinesis.connect_to_region('us-west-2')
        s = self.kinesis.describe_stream('latest_temp_data')
        s = self.kinesis.describe_stream('temp_history_dev')
        print(s)
