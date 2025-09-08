import os
import dearpygui.dearpygui as dpg
import re

from plugins.base_plugin import BasePlugin
from plugins.config_ui import ConfigUI, config_types
from plugins.data.datapoint_config import DataPointConfig
from plugins.data.data_source import DataSource
from plugins.data.sources import csv


class Data(BasePlugin):
    data: dict[str, list[any]] = {}
    dictionary: dict[str, DataPointConfig] = {}
    has_changed: bool = False
    sources: dict[str, type[DataSource]] = {
        'csv': csv.CSV
    }
    source: DataSource | None = None


    def __init__(self):
        super().__init__()
        with dpg.menu(parent='menubar', label='Data') as menu:
            config_definition = {
                'data source': config_types.Select(list(self.sources.keys()))
            }
            source_config_ui = None
            def update_config(conf):  # data source has been changed
                nonlocal source_config_ui
                if conf['data source'] == '':
                    self.source = None
                else:
                    new_source = self.sources[conf['data source']]
                    if type(self.source) != new_source:
                        self.source = new_source(self.data_changed, self.metadata_changed)
                        # create the config ui
                        dpg.delete_item(source_config_ui, children_only=True)
                        ConfigUI(source_config_ui, self.source.config_definition, self.source.config, self.source.config_changed)

            ConfigUI(menu, config_definition, {'data source': ''}, update_config)
            dpg.add_separator(label='Source config')
            source_config_ui = dpg.add_group()

    def metadata_changed(self, metadata: dict[str, DataPointConfig]):
        # called by the data source class when new metadata is available
        self.logger.info(f'New metadata {metadata}')
        for k, v in metadata.items():
            if k not in self.data:
                self.data[k] = []
                self.dictionary[k] = v

    def data_changed(self, data: dict[str, list[any]]):
        # called by the data source class when new metadata is available
        for k, v in data.items():
            self.data[k].extend(v)
        self.has_changed = True
