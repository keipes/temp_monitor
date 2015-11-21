
class TempClient():
    def __init__(self, tempfile):
        self.tempfile = tempfile
        print(tempfile)

    def refresh(self):
        with open(self.tempfile, 'r') as f:
            self.lines = f.readlines()

    def has_temp(self):
        return self.lines[0].find('YES') > -1

    def get_temp(self, convert_to_fahrenheit=True):
        temp_line = self.lines[1]
        raw_temp = float(temp_line[temp_line.rfind('=')+1:-1])
        temp_celcius = raw_temp / 1000
        if convert_to_fahrenheit:
            return (temp_celcius * 1.8) + 32
        return temp_celcius

