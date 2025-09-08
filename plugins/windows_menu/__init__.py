import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin
from utils import get_widget
from dearpygui_ext.themes import create_theme_imgui_light, create_theme_imgui_dark


class WindowsMenu(BasePlugin):
    def __init__(self):
        super().__init__()
        with dpg.menu(parent='menubar', label='Windows'):
            def change_window_parameter(_, value, key):
                for item in dpg.get_all_items():
                    widget = get_widget(item)
                    if widget:
                        dpg.configure_item(widget.window, **{key: value})

            dpg.add_menu_item(label='Hide title bar', callback=change_window_parameter, user_data='no_title_bar', check=True)
            dpg.add_menu_item(label='No background', callback=change_window_parameter, user_data='no_background', check=True)

            def toggle_theme(_, value):
                if value:
                    theme = create_theme_imgui_light()
                else:
                    theme = create_theme_imgui_dark()
                dpg.bind_theme(theme)

            dpg.add_menu_item(label='Light theme', callback=toggle_theme, check=True)
