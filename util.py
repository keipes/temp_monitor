import os

def get_temp_file():
    if is_dev_environment():
        #print(os.path.dirname(__file__))
        #return  os.path.dirname(__file__) + os.path.sep + '../dummy_tempfile'
        return 'dummy_tempfile'
    else:
        return '/sys/bus/w1/devices/28-0000071ca1ef/w1_slave'

def is_dev_environment():
    return os.uname()[0] == 'Darwin'
