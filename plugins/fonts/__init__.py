import dearpygui.dearpygui as dpg

from plugins.base_plugin import BasePlugin


class Fonts(BasePlugin):
    def __init__(self):
        with dpg.font_registry():
            self.default = dpg.add_font('neon.otf', 12)
            dpg.bind_font(self.default)
            self.big_bold = dpg.add_font('neon-bold.otf', 30, tag='big')
