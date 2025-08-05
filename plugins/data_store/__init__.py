from plugins.base_plugin import BasePlugin
import time
import math
from dataclasses import dataclass

@dataclass
class DataPointConfig:
    name: str
    type: type
    unit: str

class DataStore(BasePlugin):
    dictionary: dict[str, DataPointConfig] = {
        'accx': DataPointConfig(name='Accélération X', type=float, unit='m/s²'),
        'accy': DataPointConfig(name='Accélération Y', type=float, unit='m/s²'),
        'accz': DataPointConfig(name='Accélération Z', type=float, unit='m/s²'),
        'gyrx': DataPointConfig(name='Orientation X', type=float, unit='°'),
        'gyry': DataPointConfig(name='Orientation Y', type=float, unit='°'),
        'gyrz': DataPointConfig(name='Orientation Z', type=float, unit='°'),
        'alt': DataPointConfig(name='Altitude', type=float, unit='m'),
        'temp': DataPointConfig(name='Température', type=float, unit='°C'),
        't': DataPointConfig(name='Temps', type=float, unit='s'),
    }

    data = {}

    def __init__(self):
        # initializes data arrays for each data points
        for data_point in self.dictionary.keys():
            self.data[data_point] = []

    def render(self):
        # add random data for each datapoints
        self.data['t'].append(time.monotonic())
        for i, item in enumerate(list(self.dictionary.keys())[:-1]):
            self.data[item].append(math.sin(time.monotonic()+i))
