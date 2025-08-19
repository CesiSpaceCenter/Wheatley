import os

from plugins.base_plugin import BasePlugin
import dearpygui.dearpygui as dpg
import re
from dataclasses import dataclass

@dataclass
class DataPointConfig:
    name: str
    type: type
    unit: str

# une variable "available sources" qui prends des classes dans un dossier (une classe "csv", une classe "udp", etc)
# on doit choisir une classe de source, chaque classe construit son UI (file picker, etc)

class Data(BasePlugin):
    data: dict[str, list[any]] = {}
    dictionary: dict[str, DataPointConfig] = {}
    has_changed: bool = False
    """ = {
        'accx': DataPointConfig(name='Accélération X', type=float, unit='m/s²'),
        'accy': DataPointConfig(name='Accélération Y', type=float, unit='m/s²'),
        'accz': DataPointConfig(name='Accélération Z', type=float, unit='m/s²'),
        'gyrx': DataPointConfig(name='Orientation X', type=float, unit='°'),
        'gyry': DataPointConfig(name='Orientation Y', type=float, unit='°'),
        'gyrz': DataPointConfig(name='Orientation Z', type=float, unit='°'),
        'alt': DataPointConfig(name='Altitude', type=float, unit='m'),
        'temp': DataPointConfig(name='Température', type=float, unit='°C'),
        't': DataPointConfig(name='Temps', type=float, unit='s'),
    }"""

    def __init__(self):
        with dpg.window():
            dpg.add_slider_int(label='time window size', tag='time_window_size')
            dpg.add_slider_int(label='time window position', tag='time_window_pos')

        for file in os.listdir('data'):
            if file.endswith('.csv'):
                #print(file)
                with open('data/' + file, 'r') as f:
                    last_ts = {}
                    header = []
                    for line_num, line in enumerate(f.readlines()):
                        line = line.strip().split(',')
                        if line_num == 0:
                            for k in line:
                                name, unit, subunit = re.match(r"^(\w+)(?:\((\w+)(?:\[([^\]]*)\])?\))?$", k).groups()
                                unit = subunit if subunit is not None else (unit if unit is not None else '')
                                name = file.replace('.csv', '') + ' ' + name
                                #print('', name)
                                self.dictionary[name] = DataPointConfig(name=name, type=float, unit=unit)
                                self.data[name] = []
                                last_ts[name] = 0
                                header.append(name)
                            #print('', header)
                        else:
                            for i, k in enumerate(line):
                                name = header[i]
                                if file.replace('.csv', '') not in name:
                                    print('--- wrong filename', name, file, self.dictionary.keys(), i)
                                _type = self.dictionary[name].type
                                if 'time' in name:
                                    if _type(k) - last_ts[name] < 0:
                                        pass#print('----wrong t', k, last_ts[name])
                                    last_ts[name] = _type(k)
                                self.data[name].append(_type(k))

        self.has_changed = True


    def render(self):
        # add random data for each datapoints
        """self.data['t'].append(time.monotonic())
        for i, item in enumerate(list(self.dictionary.keys())[:-1]):
            self.data[item].append(math.sin(time.monotonic()+i))"""
