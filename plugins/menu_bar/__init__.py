import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin


class MenuBar(BasePlugin):
    def __init__(self):
        with dpg.viewport_menu_bar(tag='menubar'):
            dpg.add_menu(tag='menubar_settings', label='Settings')
