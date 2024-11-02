import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin
from uuid import uuid4


class BaseWidget(BasePlugin):
    default_config: dict
    config: dict
    default_window_config: dict
    _window_config = {
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
        self.window = window_tag

        if dpg.does_item_exist(self.window):
            # https://github.com/hoffstadt/DearPyGui/issues/1625
            # don't reconfigure label if it hasn't changed, otherwise it will break the docking
            window_config = self._window_config.copy()
            if dpg.get_item_label(self.window) == window_config['label']:
                del window_config['label']
            dpg.configure_item(self.window, **window_config, user_data=self)
            dpg.delete_item(self.window, children_only=True)
        else:
            self.window = dpg.add_window(**self._window_config, user_data=self)

        if widget_config is None:
            self.config = self.default_config
        else:
            self.config = widget_config

    @property
    def window_config(self) -> dict:
        window_config = self._window_config
        return window_config


    def render(self):
        pass

    def after_viewport(self):
        pass
