from plugins.base_plugin import BasePlugin
import time, math


class DataStore(BasePlugin):
    dictionary = {
        'accx': {
            'name': 'Accélération X',
            'type': float,
            'unit': 'm/s²'
        },
        't': {
            'name': 'Temps',
            'type': float,
            'unit': 's'
        }
    }

    data = {}

    def __init__(self):
        for data_point in self.dictionary.keys():
            self.data[data_point] = []

    def render(self):
        self.data['t'].append(time.monotonic())
        self.data['accx'].append(math.sin(time.monotonic()))