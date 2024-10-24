import json

import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin
from plugins.base_widget import BaseWidget


class WidgetConfig(BasePlugin):
    def __init__(self):
        self.window = dpg.add_window(label='Widget config', width=300, height=600)
        self.active_widget: BaseWidget = None
        self.new_widget_config: dict = None
        self.new_window_config: dict = None
        self.inputs_group = dpg.add_group(parent=self.window)
        dpg.add_button(parent=self.window, label='Save', callback=self._save_config)

    def _render_config_window(self):
        self._clear_inputs()

        dpg.add_separator(parent=self.inputs_group, label='Window config')
        for name, value in self.active_widget.window_config.items():
            if name not in ['pos', 'width', 'height']:
                self._get_input(name, value, self._update_window_config)

        dpg.add_separator(parent=self.inputs_group, label='Widget config')
        for name, value in self.active_widget.config.items():
            self._get_input(name, value, self._update_widget_config)

        dpg.add_separator(parent=self.inputs_group)

    def _get_input(self, name: str, value: any, callback: callable):
        item_config = dict(
            parent=self.inputs_group,
            label=name,
            default_value=value,
            callback=callback,
            user_data=name
        )
        match type(value).__name__:
            case 'str':
                dpg.add_input_text(**item_config)
            case 'bool':
                dpg.add_checkbox(**item_config)
            case 'int':
                dpg.add_slider_int(**item_config, max_value=1000)
            case 'float':
                dpg.add_slider_float(**item_config, max_value=1000)

    def _update_widget_config(self, _, config_value: any, config_name: str):
        self.new_widget_config[config_name] = config_value

    def _update_window_config(self, _, config_value: any, config_name: str):
        self.new_window_config[config_name] = config_value

    def _save_config(self):
        if self.active_widget is not None:
            old_widget_config = self.active_widget.config.copy()
            old_window_config = self.active_widget.window_config.copy()
            dpg.delete_item(self.active_widget.window)
            type(self.active_widget)(
                {**old_window_config, **self.new_window_config},
                {**old_widget_config, **self.new_widget_config}
            )

    def _clear_inputs(self):
        for item in dpg.get_item_children(self.inputs_group, 1):
            dpg.delete_item(item)

    def render(self):
        active_window = dpg.get_active_window()
        if active_window == self.window:
            return
        if active_window > 10 and isinstance(dpg.get_item_user_data(active_window), BaseWidget):
            widget = dpg.get_item_user_data(active_window)
            if self.active_widget != widget:
                self.new_widget_config = {}
                self.new_window_config = {}
                self.active_widget = widget
                self._render_config_window()
        elif self.active_widget is not None:
            self.active_widget = None
            self._clear_inputs()
