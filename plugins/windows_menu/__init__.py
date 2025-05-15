import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin
from utils import get_widget


class WindowsMenu(BasePlugin):
    def __init__(self):
        with dpg.menu(parent='menubar', label='Windows'):
            def change_window_parameter(_, value, key):
                for item in dpg.get_all_items():
                    widget = get_widget(item)
                    if widget:
                        dpg.configure_item(widget.window, **{key: value})

            dpg.add_menu_item(label='Hide title bar', callback=change_window_parameter, user_data='no_title_bar', check=True)
            dpg.add_menu_item(label='No background', callback=change_window_parameter, user_data='no_background', check=True)
