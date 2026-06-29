import socket
import time
from typing import Any

from plugins.config_ui import config_types
from plugins.data.datapoint_config import DataPoint
from plugins.data.data_source import DataSource


class UDP(DataSource):
    config_definition = {
        'host': config_types.Str(default='localhost'),
        'port': config_types.Int()
    }

    config = {
        'host': 'localhost',
        'port': 47269
    }

    dictionary = {}

    sock: socket.socket | None = None
    connected = False

    def config_changed(self, config: dict[str, Any]):
        self.config = config
        # reconnect
        self.disconnect()
        self.connect()

    def loop(self):
        first_line = True
        while self.run:
            if self.connected:
                try:
                    line = self.sock.recv(1024, socket.MSG_WAITALL).decode()
                    assert len(line) > 0
                except Exception as e:
                    self.logger.error(e)
                    break
                #print(line)

                if not line.startswith('>'):
                    for variable in line.split(','):
                        variable_name = variable.split(':')[0]
                        value = float(variable.split(':')[1])
                        if variable_name not in self.dictionary:
                            self.dictionary[variable_name] = DataPoint(name=variable_name, type=float, unit='')
                            self.metadata_changed_callback(self.dictionary)

                        self.data_changed_callback({variable_name: [value]})
                else:
                    self.logger.info(f'Log from remote: {line}')

    def connect(self):
        self.logger.info(f'Connecting to {self.config['host']}:{self.config['port']}')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.config['host'], self.config['port']))
        self.logger.info('Connected')
        self.connected = True

    def disconnect(self):
        self.logger.info(f'Disconnecting')
        if self.sock is None:
            return

        self.connected = False
        self.sock.sendto(b' ', (self.config['host'], self.config['port']))
        self.sock.close()
        time.sleep(1)
        self.sock = None

        self.logger.info('Disconnected')
