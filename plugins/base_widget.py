import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin


class BaseWidget(BasePlugin):
    config: dict
    default_window_config: dict
    _window_config: dict
    window: int

    def __init__(self, window_config=None, widget_config=None):
        if window_config is None:
            self._window_config = self.default_window_config
        else:
            self._window_config = window_config
        self.window = dpg.add_window(**self._window_config, user_data=self)
        if widget_config is not None:
            self.config = widget_config

    @property
    def window_config(self) -> dict:
        window_config = self._window_config
        window_config['width'] = dpg.get_item_width(self.window)
        window_config['height'] = dpg.get_item_height(self.window)
        window_config['pos'] = dpg.get_item_pos(self.window)
        return window_config


    def render(self):
        pass

    def after_viewport(self):
        pass
