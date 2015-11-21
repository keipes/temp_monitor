from client.temp import TempClient
import util

if __name__ == '__main__':
    tm = TempClient(util.get_temp_file())
    print('has temp? ' + str(tm.has_temp()))
    print(tm.get_temp())
