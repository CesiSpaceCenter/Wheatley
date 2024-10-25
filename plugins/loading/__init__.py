import dearpygui.dearpygui as dpg

from plugins.base_plugin import BasePlugin


class Loading(BasePlugin):
    window: int | str

    def __init__(self):
        with dpg.window(no_move=True, no_close=True, no_resize=True, no_title_bar=True, modal=True, show=False, min_size=(0, 0)) as self.window:
            dpg.add_loading_indicator()

    def open(self):
        dpg.show_item(self.window)

    def close(self):
        dpg.hide_item(self.window)