import dearpygui.dearpygui as dpg
from typing import Any
import logging

from plugins.config_ui import config_types

# this plugin does not instance the BasePlugin class, because it is just a utility class, and will be instantiated
# and initiated multiple times in various places

class ConfigUI:
    def __init__(self, parent: int | str, definition: dict[str, config_types.Base], default_values: dict[str, Any], save_callback: callable):
        self.logger = logging.getLogger(f'ConfigUI#{hex(id(self))}')
        self.definition = definition
        self.values = default_values

        self.logger.debug(f'definition: {definition} default: {self.values}')

        def callback(_, config_value, config_name):
            config_type = self.definition[config_name]
            self.values[config_name] = config_type.parse(config_value)

        for name, value in self.values.items():
            self.definition[name].ui(parent, name, value, callback)
        dpg.add_separator(parent=parent)
        dpg.add_button(parent=parent, label='Save', callback=lambda: save_callback(self.values), width=-1)
