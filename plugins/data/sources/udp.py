import re
import socket
from io import TextIOWrapper

from plugins.config_ui import config_types
from plugins.data.datapoint_config import DataPointConfig
from plugins.data.data_source import DataSource
from plugins.loading import Loading


class UDP(DataSource):
    config_definition = {
        'host': config_types.Str(default='localhost'),
        'port': config_types.Int(),
        'datapoints': config_types.List(config_types.Group({
            'name': config_types.Str(),
            'unit': config_types.Str(),
            'type': config_types.Select(['int', 'float'], default='int')
        }))
    }

    config = {
        'host': 'localhost',
        'port': 0,
        'datapoints': []
    }

    dictionary: dict[str, DataPointConfig] = {}

    sock: socket.socket | None = None
    stream: TextIOWrapper | None = None
    connected = False

    def config_changed(self, config: dict[str, any]):
        self.config = config
        for datapoint in config['datapoints']:
            self.dictionary[datapoint['name']] = DataPointConfig(
                name=datapoint['name'],
                unit=datapoint['unit'],
                type={'int': int, 'float': float}[datapoint['type']]
            )
        self.metadata_changed_callback(self.dictionary)

        # reconnect
        self.disconnect()
        self.connect()

    def loop(self):
        first_line = True
        while True:
            if self.connected:
                cols = self.stream.readline().strip().split(b'\t')
                print(cols)
                data = {}
                for i, v in enumerate(cols):
                    if len(v.decode().split(':')) != 2:
                        continue
                    key = v.decode().split(':')[0]
                    value = v.decode().split(':')[1]
                    if ' ' in value:
                        value = value.split(' ')[0]
                    if first_line and key not in self.dictionary:
                        self.dictionary[key] = DataPointConfig(
                            name=key,
                            unit=key,
                            type=float
                        )
                    name = self.dictionary[key].name
                    _type = self.dictionary[name].type
                    data[name] = [_type(value)]
                if first_line:
                    self.metadata_changed_callback(self.dictionary)
                    first_line = False
                self.data_changed_callback(data)

    def connect(self):
        self.logger.info(f'Connecting to {self.config['host']}:{self.config['port']}')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.config['host'], self.config['port']))
        self.stream = self.sock.makefile('rb', 1024)
        self.connected = True

    def disconnect(self):
        self.logger.info(f'Disconnecting {self.config['host']}:{self.config['port']}')
        self.connected = False
        if self.sock is not None:
            self.sock.close()
            self.sock = None
        if self.stream is not None:
            self.stream.close()
            self.stream = None
