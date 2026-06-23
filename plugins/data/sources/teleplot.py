import re
from typing import Optional, Any
import serial as pyserial
import dearpygui.dearpygui as dpg
from plugins.config_ui import config_types
from plugins.data.datapoint_config import DataPointConfig
from plugins.data.data_source import DataSource
from plugins.loading import Loading


class Teleplot(DataSource):
    config_definition = {
        'port': config_types.Str(),
        'baud': config_types.Int()
    }

    config = {
        'port': '/dev/ttyACM0',
        'baud': 115200
    }

    dictionary = {}

    serial: Optional[pyserial.Serial] = None

    def config_changed(self, config: dict[str, Any]):
        self.config = config

        self.logger.info(f'Opening serial port {self.config['port']} {self.config['baud']}')

        Loading.plugin.open()
        if self.serial is not None:
            self.serial.close()
        try:
            self.serial = pyserial.Serial(self.config['port'], self.config['baud'])
        except pyserial.serialutil.SerialException as e:
            with dpg.window():
                dpg.add_text(f'Error while opening serial port\n{e}')
            raise
        Loading.plugin.close()

    def loop(self):
        while self.run:
            if self.serial is not None and self.serial.is_open:
                line = self.serial.readline().decode().strip()
                if line.startswith('>'):
                    line = line[1:]  # remove starting ">"
                    for variable in line.split(','):
                        variable_name = variable.split(':')[0]
                        value = float(variable.split(':')[1])
                        if variable_name not in self.dictionary:
                            self.dictionary[variable_name] = DataPointConfig(name=variable_name, type=float, unit='')
                            self.metadata_changed_callback(self.dictionary)

                        self.data_changed_callback({variable_name: [value]})
                else:
                    self.logger.info(f'Log from remote: {line}')


    def okokokkkokkokokok(self):
        with open(self.config['file'], 'r') as f:
            header = []
            data = {}
            for line_num, line in enumerate(f.readlines()):
                cols = line.strip().split(',')
                if line_num == 0:  # header line
                    for k in cols:
                        name, unit, subunit = re.match(r"^(?:#\ )?(\w+)(?:\(?(\w*)(?:\[([^\]]*)\])?\)?)?", k).groups()
                        unit = subunit if subunit is not None else (unit if unit is not None else '')
                        if name not in header:
                            self.dictionary[name] = DataPointConfig(name=name, type=float, unit=unit)
                            print(' ', name, unit)
                            header.append(name)
                            data[name] = []
                else:
                    for i, k in enumerate(cols):
                        name = list(self.dictionary.values())[i].name
                        _type = self.dictionary[name].type
                        data[name].append(_type(k))
            self.logger.info(f'Done loading CSV, {len(header)} columns, {len(data[header[0]])} rows')
            self.metadata_changed_callback(self.dictionary)
            self.data_changed_callback(data)
            Loading.plugin.close()

    def close(self):
        if self.serial is not None:
            self.serial.close()