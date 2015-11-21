import os
import boto
import time

class TempMonitor():
    def __init__(self, tempfile):
        self.tempfile = tempfile
        print(tempfile)

    def refresh(self):
        with open(self.tempfile, 'r') as f:
            self.lines = f.readlines()

    def has_temp(self):
        return self.lines[0].find('YES') > -1

    def get_temp(self, convert_to_fahrenheit=True):
        temp_line = self.lines[1]
        raw_temp = float(temp_line[temp_line.rfind('=')+1:-1])
        temp_celcius = raw_temp / 1000
        if convert_to_fahrenheit:
            return (temp_celcius * 1.8) + 32
        return temp_celcius

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



def main():
    if os.uname()[0] == 'Darwin':
        tempfile = os.path.dirname(__file__) + os.path.sep + 'dummy_tempfile'
    else:
        tempfile = '/sys/bus/w1/devices/28-0000071ca1ef/w1_slave'
    tm = TempMonitor(tempfile)
    dc = DynamoClient()
    while (True):
        tm.refresh()
        if (tm.has_temp()):
            dc.record_temperature(tm.get_temp())
        print(tm.get_temp())
        time.sleep(60)

if __name__ == '__main__':
    main()

