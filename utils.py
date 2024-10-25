import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget


def get_widget(item: (int | str)) -> None | BaseWidget:
    user_data = dpg.get_item_user_data(item)
    if isinstance(user_data, BaseWidget):
        return user_data
    return None
