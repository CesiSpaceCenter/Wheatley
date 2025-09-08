import dearpygui.dearpygui as dpg
from os import path

from plugins.base_plugin import BasePlugin


class Fonts(BasePlugin):
    def __init__(self):
        super().__init__()
        with dpg.font_registry():
            basepath = path.dirname(__file__)
            self.default = dpg.add_font(path.join(basepath, 'neon.otf'), 12)
            dpg.bind_font(self.default)
            self.big_bold = dpg.add_font(path.join(basepath, 'neon-bold.otf'), 30, tag='big')
