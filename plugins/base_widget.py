import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin
from uuid import uuid4


class BaseWidget(BasePlugin):
    default_config: dict
    config: dict
    default_window_config: dict
    _window_config = {
        'pos': (100, 100),
        'min_size': (0, 0),
        'width': 300,
        'height': 200,
        'label': 'Widget',
        'no_scrollbar': False,
        'no_scroll_with_mouse': False
    }
    window: int

    ready = False

    def __init__(self, window_config=None, widget_config=None, window_tag=None):
        if window_config is None:
            self._window_config = {**self._window_config, **self.default_window_config}
        else:
            self._window_config = {**self._window_config, **window_config}

        if window_tag is None:
            window_tag = uuid4().hex

        self.window = dpg.add_window(**self._window_config, user_data=self, tag=window_tag)

        if widget_config is None:
            self.config = self.default_config
        else:
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
