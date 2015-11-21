from client.dynamo import DynamoClient

def main():
    dc = DynamoClient()
    temp = dc.get_latest_temperature()
    print(temp['temperature'])

if __name__ == '__main__':
    main()

