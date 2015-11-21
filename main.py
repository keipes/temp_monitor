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
        if (tm.has_temp()):
            pass
            #dc.record_temperature(tm.get_temp())
        print(tm.get_temp())
        time.sleep(1)

if __name__ == '__main__':
    main()

