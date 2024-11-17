import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget


def get_widget(item: (int | str)) -> None | BaseWidget:
    # tags 0 to 10 are reserved for dpg internal items, and get_item_user_data returns an error
    if isinstance(item, int) and item <= 10:
        return None
    user_data = dpg.get_item_user_data(item)
    if isinstance(user_data, BaseWidget):
        return user_data
    return None
