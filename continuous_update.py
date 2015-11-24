import os
import boto
import time
import util
from client.temp import TempClient
from client.dynamo import DynamoClient

def main():
    tempfile = util.get_temp_file()
    tm = TempClient(tempfile)
    table = util.get_temp_hist_table()
    print(table)
    dc = DynamoClient(table)
    while (True):
        s_time = time.time()
        tm.refresh()
        temp = tm.get_temp()
        if (tm.has_temp()):
            dc.record_temperature(temp)
        print(temp)
        sleep_time = 1 - (time.time() - s_time)
        print(sleep_time)
        time.sleep(sleep_time)

if __name__ == '__main__':
    main()

