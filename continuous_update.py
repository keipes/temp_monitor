import os
import boto
import time
import util
from client.temp import TempClient
from client.dynamo import DynamoClient

def main():
    tempfile = util.get_temp_file()
    tm = TempClient(tempfile)
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

