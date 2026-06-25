from os.path import basename
from typing import Any, Literal
import copy
import dearpygui.dearpygui as dpg
import filedialpy


class Base:
    _default: Any
    base_default: Any = None
    config: Any

    def default(self):
        # returns either a new copy of self._default (default value of the config item represented by this type),
        # or a new copy of self.base_default (default value of this type)
        return copy.deepcopy(self._default if self._default is not None else self.base_default)

    def __init__(self, config=None, default=None):
        self._default = default
        self.config = config if config is not None else {}

    def parse(self, val: Any):
        pass

    def ui(self, parent, name: str, value: Any, callback):
        pass


class List(Base):
    """
    A growable list of a subconfig item

    `config` represent the config_type of the subitems
    """
    base_default = []
    config: Base

    def parse(self, val: Any):
        return list(val)

    def ui(self, parent, name: str, value: Any, callback):
        list_group = dpg.add_tree_node(label=name, parent=parent, default_open=True)

        def build_ui():
            dpg.delete_item(list_group, children_only=True)  # clear all previous elements
            for i, item_value in enumerate(value):  # create new ones
                def list_callback(_, new_item_value, index):
                    # update the value list and call the callback
                    value[int(index)] = new_item_value
                    callback(None, value, name)

                item_group = dpg.add_group(parent=list_group, horizontal=True)
                def remove_item_callback(_a, _b, index):
                    # remove the item and rebuild the ui
                    del value[index]
                    callback(None, value, name)
                    build_ui()

                with dpg.theme() as item_theme:
                    with dpg.theme_component(dpg.mvButton):
                        btn = dpg.add_button(label='×', callback=remove_item_callback, user_data=int(i), parent=item_group)
                        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 120), category=dpg.mvThemeCat_Core)
                    dpg.bind_item_theme(btn, item_theme)
                #ConfigUI.get_input(str(i), item_value, subitem_type, list_callback, item_group)
                #(name: str, value: Any, config_item: config_types.Base, callback: callable, parent: int):
                self.config.ui(item_group, str(i), item_value, list_callback)  # self.config is the subitem config type
        build_ui()

        def add_item_callback():
            # add an empty new value and rebuild the ui
            a=self.config.default()
            value.append(a)
            callback(None, value, name)
            build_ui()
        dpg.add_button(label=f'Add to {name}', width=-1, callback=add_item_callback, parent=parent)


class Select(Base):
    """
    A combobox with choices to choose from

    `config` is a list of any type representing the choices
    """
    base_default = None
    config: list[Any]

    def parse(self, val: Any):
        return val

    def ui(self, parent, name: str, value: Any, callback):
        # config are the subitems
        dpg.add_combo(
            self.config,
            parent=parent,
            label=name,
            default_value=value,
            callback=callback,
            user_data=name
        )


class DataPoint(Base):
    """
    A datapoint to choose from the 'data' plugin dictionary
    """
    base_default = ''

    def parse(self, val: Any):
        return str(val)

    def ui(self, parent, name: str, value: str, callback):
        from plugins.data import Data
        dpg.add_combo(
            [d for d in Data.plugin.dictionary.keys()],
            parent=parent,
            label=name,
            default_value=value,
            callback=callback,
            user_data=name
        )


class Group(Base):
    """
    A group of subconfig items

    `config` is like widget.config_definition, a dict with the config item name as the key
    and the config_type as the value
    """
    base_default = None
    config: dict[str, Base]

    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)
        if self.default() is None:
            self._default = {}
            for k, v in self.config.items():
                self._default[k] = v.default()

    def parse(self, val: Any):
        return dict(val)

    def ui(self, parent, name: str, value: dict[str, Any], callback):
        item_group = dpg.add_tree_node(label=name, parent=parent, default_open=True)
        for item_name, item_type in self.config.items():  # self.config are the subitems key & config type
            item_value = value[item_name]

            def list_callback(_, new_item_value, item_name):
                # update the value list and call the callback
                value[item_name] = new_item_value
                callback(None, value, name)

            item_type.ui(item_group, item_name, item_value, list_callback)


class Str(Base):
    """
    A plain string (input)

    `config` is a dict:
    - multiline (bool): If true, allows multiline editing
    """
    base_default = ''
    config: dict[Literal['multiline'], Any]

    def parse(self, val: Any):
        return str(val)

    def ui(self, parent, name: str, value: str, callback):
        dpg.add_input_text(
            parent=parent,
            label=name,
            default_value=value,
            callback=callback,
            user_data=name,
            multiline=self.config.get('multiline', False)
        )


class Int(Base):
    """
    A simple integer (input)
    """
    base_default = 0

    def parse(self, val: Any):
        return int(val)

    def ui(self, parent, name: str, value: int, callback):
        dpg.add_input_int(
            parent=parent,
            label=name,
            default_value=value,
            callback=callback,
            user_data=name
        )


class Float(Base):
    """
    A simple float (input)
    """
    base_default = 0.0

    def parse(self, val: Any):
        return float(val)

    def ui(self, parent, name: str, value: float, callback):
        dpg.add_input_float(
            parent=parent,
            label=name,
            default_value=value,
            callback=callback,
            user_data=name
        )


class Bool(Base):
    """
    A simple boolean (checkbox)
    """
    base_default = False

    def parse(self, val: Any):
        return bool(val)

    def ui(self, parent, name: str, value: bool, callback):
        dpg.add_checkbox(
            parent=parent,
            label=name,
            default_value=value,
            callback=callback,
            user_data=name
        )


class Text(Base):
    """
    A readonly text, not an actual input
    The displayed text is the key/name of this config item
    """
    def ui(self, parent, name: str, value: Any, callback):
        dpg.add_text(name, parent=parent)


class File(Base):
    """
    A file path, selected by a file picker
    """
    base_default = ''

    def parse(self, val: Any):
        return str(val)

    def ui(self, parent, name: str, value: Any, callback):
        with dpg.group(horizontal=True, parent=parent):
            path_text = dpg.add_text()

            def file_callback():
                path = filedialpy.openFile()
                dpg.set_value(path_text, basename(path))
                callback(None, path, name)

            dpg.add_button(label='Open file', callback=file_callback)
            dpg.add_text(default_value=name)


class Color(Base):
    """
    A RGB color to choose with a color picker
    """
    base_default = (0, 0, 0)

    def parse(self, val: list):
        return (val[0]*255, val[1]*255, val[2]*255)

    def ui(self, parent, name: str, value: tuple, callback):
        dpg.add_color_edit(
            parent=parent,
            label=name,
            default_value=value,
            callback=callback,
            user_data=name,
            no_alpha=True
        )