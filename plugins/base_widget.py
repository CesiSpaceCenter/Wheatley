import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin


class BaseWidget(BasePlugin):
    config: dict
    window_config: dict
    window: int

    def __init__(self, window_config=None, widget_config=None):
        if window_config is None:
            self.window = dpg.add_window(user_data=self)
        else:
            self.window = dpg.add_window(**self.window_config, user_data=self)
        if widget_config is not None:
            self.config = widget_config

    def config_updated(self, config_name: str, config_value: any):
        pass

    def render(self):
        pass

    def after_viewport(self):
        pass
