import os

def is_dev_environment():
    return os.uname()[0] == 'Darwin'

if is_dev_environment():
    temp_hist_arn = 'arn:aws:dynamodb:us-west-2:630535199163:table/temp_history_dev/stream/2015-11-21T11:42:26.677'
else:
    temp_hist_arn = 'arn:aws:dynamodb:us-west-2:630535199163:table/temp_history/stream/2015-11-21T12:12:53.316'
misc_arn = 'arn:aws:dynamodb:us-west-2:630535199163:table/miscellaneous/stream/2015-11-22T07:23:48.068'

def get_temp_file():
    if is_dev_environment():
        #print(os.path.dirname(__file__))
        #return  os.path.dirname(__file__) + os.path.sep + '../dummy_tempfile'
        return 'data/dummy_tempfile'
    else:
        return '/sys/bus/w1/devices/28-0000071ca1ef/w1_slave'

def get_temp_hist_table():
    if is_dev_environment():
        return 'temp_history_dev'
    else:
        return 'temp_history'
