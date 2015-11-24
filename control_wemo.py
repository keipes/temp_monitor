from client.wemo import WemoClient
from client.dynamo import DynamoClient
from client.dynamostream import DynamoStreamClient
import time
import util
import Queue

def main():
  wc = WemoClient()
  dc = DynamoClient('miscellaneous')
  queue = Queue.Queue()
  queue_list = [queue]
  old_items = []
  dsc = DynamoStreamClient(queue_list, old_items, util.temp_hist_arn)
  dsc.start()
  try:
      while True:
        max_temp = dc.get_max_temp()
        min_temp = dc.get_min_temp()
        d = queue.get()
        temp = d['temperature']
        if temp > max_temp:
          wc.switch_off()
        elif temp < min_temp:
          wc.switch_on()
  finally:
    dsc.stop()





if __name__ == '__main__':
    main()