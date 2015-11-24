import os
import boto
import time
import util
from client.temp import TempClient
from client.dynamo import DynamoClient

def main():
    try:
        print('starting updates')
        do_them_updates()
    except Exception:
        time.sleep(10)
        main()

def do_them_updates():
    tempfile = util.get_temp_file()
    tm = TempClient(tempfile)
    table = util.get_temp_hist_table()
    dc = DynamoClient(table)
    while (True):
        s_time = time.time()
        tm.refresh()
        temp = tm.get_temp()
        if (tm.has_temp()):
            dc.record_temperature(temp)
        sleep_time = 1 - (time.time() - s_time)
        time.sleep(sleep_time)

if __name__ == '__main__':
    main()

