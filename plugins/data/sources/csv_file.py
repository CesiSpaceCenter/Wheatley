import re
import os

from plugins.config_ui import config_types
from plugins.data.datapoint_config import DataPointConfig
from plugins.data.data_source import DataSource
from plugins.loading import Loading


class CSV(DataSource):
    config_definition = {
        'file': config_types.File(),
        'newline separator': config_types.Str(default='\n'),
        'cell separator': config_types.Str(default=',')
    }

    config = {
        'file': '',
        'newline separator': '\n',
        'cell separator': ','
    }

    dictionary = {}

    def config_changed(self, config: dict[str, any]):
        self.config = config

        if not os.path.exists(self.config['file']):
            return

        Loading.plugin.open()

        self.logger.info(f'Opening {self.config['file']}')

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
