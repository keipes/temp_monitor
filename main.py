import os
import boto
import time
from temp_monitor import TempMonitor
from dynamo_client import DynamoClient

def main():
    if os.uname()[0] == 'Darwin':
        tempfile = os.path.dirname(__file__) + os.path.sep + 'dummy_tempfile'
    else:
        tempfile = '/sys/bus/w1/devices/28-0000071ca1ef/w1_slave'
    tm = TempMonitor(tempfile)
    dc = DynamoClient()
    while (True):
        tm.refresh()
        temp = tm.get_temp()
        if (tm.has_temp()):
            if (os.uname()[0] != 'Darwin'):
                dc.record_temperature(temp)
        print(temp)
        time.sleep(1)

if __name__ == '__main__':
    main()

