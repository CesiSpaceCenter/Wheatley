import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin


class MenuBar(BasePlugin):
    def __init__(self):
        super().__init__()
        dpg.add_viewport_menu_bar(tag='menubar')
