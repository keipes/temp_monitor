from client.dynamo import DynamoClient
import util

def main():
    table = util.get_temp_hist_table()
    dc = DynamoClient()
    temp = dc.get_latest_temperature()
    print(temp['temperature'])

if __name__ == '__main__':
    main()

