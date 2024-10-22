import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin
from plugins.base_widget import BaseWidget


class WidgetConfig(BasePlugin):
    def __init__(self):
        self.window = dpg.add_window(label='Widget config', width=300, height=600)
        self.active_widget = None
        self.current_config = None
        self.inputs_group = dpg.add_group(parent=self.window)
        dpg.add_button(parent=self.window, label='Save', callback=self._save_config)

    def _render_config_window(self):
        self._clear_config_window()
        for config_name, config_value in self.current_config.items():
            match type(config_value).__name__:
                case 'str':
                    dpg.add_input_text(
                        parent=self.inputs_group,
                        label=config_name,
                        default_value=config_value,
                        callback=self._update_config,
                        user_data=config_name
                    )
                case 'bool':
                    dpg.add_checkbox(
                        parent=self.inputs_group,
                        label=config_name,
                        default_value=config_value,
                        callback=self._update_config,
                        user_data=config_name
                    )

    def _update_config(self, _, config_value, config_name):
        self.current_config[config_name] = config_value

    def _save_config(self):
        if self.active_widget is not None:
            self.active_widget.__class__(self.active_widget.window_config, self.current_config)
            dpg.delete_item(self.active_widget.window)

    def _clear_config_window(self):
        for item in dpg.get_item_children(self.inputs_group, 1):
            dpg.delete_item(item)

    def render(self):
        active_window = dpg.get_active_window()
        if active_window == self.window:
            return
        if active_window != 0 and isinstance(dpg.get_item_user_data(active_window), BaseWidget):
            widget = dpg.get_item_user_data(active_window)
            if self.active_widget != widget:
                self.current_config = widget.config.copy()
                self.active_widget = widget
                self._render_config_window()
        elif self.active_widget is not None:
            self.active_widget = None
            self._clear_config_window()
