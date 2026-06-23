import dearpygui.dearpygui as dpg
from typing import Any

from plugins.base_plugin import BasePlugin
from plugins.config_ui import ConfigUI, config_types
from plugins.data.datapoint_config import DataPointConfig
from plugins.data.data_source import DataSource
from plugins.data.sources import csv_file, teleplot#, udp


class Data(BasePlugin):
    data: dict[str, list[Any]] = {}
    dictionary: dict[str, DataPointConfig] = {}
    has_changed: bool = False
    sources: dict[str, type[DataSource]] = {
        'CSV file': csv_file.CSV,
        'Teleplot': teleplot.Teleplot
        #'UDP': udp.UDP
    }
    source: DataSource | None = None
    history_size = 1000


    def __init__(self):
        super().__init__()
        with dpg.menu(parent='menubar', label='Data') as menu:
            def source_changed(_, source):
                if self.source is not None:
                    self.source.stop()
                if source == '':
                    self.source = None
                else:
                    new_source = self.sources[source]
                    if type(self.source) != new_source:
                        self.source = new_source(self.data_changed, self.metadata_changed)
                        # create the config ui
                        dpg.delete_item(source_config_ui, children_only=True)
                        ConfigUI(source_config_ui, self.source.config_definition, self.source.config,
                                 self.source.config_changed)
            dpg.add_combo(label='Data source', items=list(self.sources.keys()), callback=source_changed)

            def history_size_changed(_, size):
                self.history_size = size
            dpg.add_input_int(label='History size', min_value=-1, default_value=self.history_size, callback=history_size_changed)

            dpg.add_separator(label='Source config')
            source_config_ui = dpg.add_group()

    def metadata_changed(self, metadata: dict[str, DataPointConfig]):
        # called by the data source class when new metadata is available
        self.logger.info(f'New metadata {metadata}')
        for k, v in metadata.items():
            self.data[k] = []
            self.dictionary[k] = v

    def data_changed(self, data: dict[str, list[Any]]):
        # called by the data source class when new metadata is available
        for k, v in data.items():
            self.data[k].extend(v)
            if len(self.data[k]) > self.history_size:
                self.data[k] = self.data[k][-self.history_size:]
        self.has_changed = True

    def stop(self):
        if self.source is not None:
            self.source.stop()

