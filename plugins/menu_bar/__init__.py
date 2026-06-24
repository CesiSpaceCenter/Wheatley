import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin


class MenuBar(BasePlugin):
    def __init__(self, *args):
        super().__init__(*args)
        dpg.add_viewport_menu_bar(tag='menubar')
