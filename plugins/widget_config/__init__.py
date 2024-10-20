import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin
from plugins.base_widget import BaseWidget


class WidgetConfig(BasePlugin):
    def __init__(self):
        self.window = dpg.add_window(label='Widget config', width=300, height=600)
        self.active_widget = None

    def _render_config_window(self):
        for config_name, config_value in self.active_widget.config.items():
            match type(config_value).__name__:
                case 'str':
                    dpg.add_input_text(
                        parent=self.window,
                        label=config_name,
                        default_value=config_value,
                        callback=self._update_config,
                        user_data=config_name
                    )
                case 'bool':
                    dpg.add_checkbox(
                        parent=self.window,
                        label=config_name,
                        default_value=config_value,
                        callback=self._update_config,
                        user_data=config_name
                    )

    def _update_config(self, _, config_value, config_name):
        self.active_widget.config[config_name] = config_value
        self.active_widget.config_updated(config_name, config_value)

    def _clear_config_window(self):
        print(dpg.get_item_children(self.window, 1))
        for item in dpg.get_item_children(self.window, 1):
            dpg.delete_item(item)

    def render(self):
        active_window = dpg.get_active_window()
        if active_window == self.window:
            return
        if active_window != 0 and isinstance(dpg.get_item_user_data(active_window), BaseWidget):
            widget = dpg.get_item_user_data(active_window)
            if self.active_widget != widget:
                self.active_widget = widget
                self._render_config_window()
        else:
            if self.active_widget is not None:
                self.active_widget = None
                self._clear_config_window()
