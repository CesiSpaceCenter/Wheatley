import dearpygui.dearpygui as dpg
from copy import deepcopy

from plugins.data import Data
from plugins.config_ui import config_types

class ConfigUI:
    def __init__(self, parent: int | str, definition: dict[str, config_types.Base], default_values: dict[str, any], save_callback: callable):
        self.definition = definition
        self.values = deepcopy(default_values)

        def callback(_, config_value, config_name):
            config_type = self.definition[config_name].parse
            self.values[config_name] = config_type(config_value)

        for name, value in self.values.items():
            self.get_input(name, value, self.definition[name], callback, parent)
        dpg.add_separator(parent=parent)
        dpg.add_button(parent=parent, label='Save', callback=lambda: save_callback(self.values), width=-1)

    @staticmethod
    def get_input(name: str, value: any, config_item: config_types.Base, callback: callable, parent: int):
        """ creates an input depending on the value's type """
        item_config = dict(  # common config for all inputs
            parent=parent,
            label=name,
            default_value=value,
            callback=callback,
            user_data=name
        )
        match type(config_item).__name__:  # depending on the type of this config item
            case 'Text':
                dpg.add_text(name, parent=parent)
            case 'Str':
                dpg.add_input_text(**item_config, multiline=config_item.config.get('multiline', False))
            case 'Bool':
                dpg.add_checkbox(**item_config)
            case 'Int':
                dpg.add_input_int(**item_config)
            case 'Float':
                dpg.add_input_float(**item_config)
            case 'DataPoint':
                dpg.add_combo([d for d in Data.plugin.dictionary.keys()], **item_config)
            case 'List':
                subitem_type: config_types.Base = config_item.config
                list_group = dpg.add_tree_node(label=name, parent=parent, default_open=True)
                def build_ui():
                    dpg.delete_item(list_group, children_only=True)  # clear all previous elements
                    for i, item_value in enumerate(value):  # create new ones
                        def list_callback(_, new_item_value, index):
                            # update the value list and call the callback
                            value[int(index)] = new_item_value
                            callback(None, value, name)
                        item_group = dpg.add_group(parent=list_group, horizontal=True)
                        ConfigUI.get_input(str(i), item_value, subitem_type, list_callback, item_group)

                        def remove_item_callback(_a, _b, index):
                            # remove the item and rebuild the ui
                            del value[index]
                            callback(None, value, name)
                            build_ui()
                        dpg.add_button(label='Remove', callback=remove_item_callback, user_data=int(i), parent=item_group)
                build_ui()

                def add_item_callback():
                    # add an empty new value and rebuild the ui
                    a=subitem_type.default()
                    value.append(a)
                    callback(None, value, name)
                    build_ui()
                dpg.add_button(label=f'Add to {name}', width=-1, callback=add_item_callback, parent=parent)

            case 'Group':
                subitems: dict[str, config_types.Base] = config_item.config
                item_group = dpg.add_tree_node(label=name, parent=parent, default_open=True)
                for item_name, item_type in subitems.items():
                    item_value = value[item_name]
                    def list_callback(_, new_item_value, item_name):
                        # update the value list and call the callback
                        value[item_name] = new_item_value
                        callback(None, value, name)
                    ConfigUI.get_input(item_name, item_value, item_type, list_callback, item_group)