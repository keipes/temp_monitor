from ouimeaux.environment import Environment
import time

class WemoClient():
    def __init__(self):
        self.env = Environment(_on_switch, _on_motion)
        self.env.start()
        self.env.discover(4)

    def toggle(self):
        _switch_map.values()[0].toggle()

_switch_map = {}
def _on_switch(switch):
    print(switch.explain())
    _switch_map[switch.serialnumber] = switch

def _on_motion(motion):
    pass

if __name__ == '__main__':
    wc = WemoClient()
    wc.toggle()

