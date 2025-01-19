from plugins.base_plugin import BasePlugin
import time
import math


class DataPoint(str):  # used by widget_config to indentify a data point
    pass


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
        # initializes data arrays for each data points
        for data_point in self.dictionary.keys():
            self.data[data_point] = []

    def render(self):
        # add random data for each datapoints
        self.data['t'].append(time.monotonic())
        self.data['accx'].append(math.sin(time.monotonic()))
