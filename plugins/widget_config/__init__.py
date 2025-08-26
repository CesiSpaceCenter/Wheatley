import dearpygui.dearpygui as dpg
from copy import deepcopy

from plugins.base_plugin import BasePlugin
from plugins.data import Data
from utils import get_widget
from plugins.base_widget import BaseWidget, Types

class WidgetConfig(BasePlugin):
    def __init__(self):
        self.window = dpg.add_window(label='Widget config', width=300, height=600)
        self.active_widget: BaseWidget = None
        # the next 2 dict will store the temporary new config. they are updated in real-time with the inputs
        self.new_widget_config: dict = None
        self.new_window_config: dict = None
        self.inputs_group = dpg.add_group(parent=self.window)  # group where all the dynamic inputs will be

    def render_config_window(self):
        """ Re-create inputs depending on the selected widget's config """
        dpg.delete_item(self.inputs_group, children_only=True)  # remove all existing inputs

        def update_window_config(_, config_value: any, config_name: str):  # callback for when a window config input is updated
            config_type = self.active_widget.window_config_definition[config_name].parse
            self.new_window_config[config_name] = config_type(config_value)

        # create inputs for the widget's window config
        dpg.add_separator(parent=self.inputs_group, label='Window config')
        for name, value in deepcopy(self.active_widget.window_config).items():
            self.get_input(name, value, self.active_widget.window_config_definition[name], update_window_config)

        def update_widget_config(_, config_value: any, config_name: str):  # callback for when a widget config input is updated
            config_type = self.active_widget.config_definition[config_name].parse
            self.new_widget_config[config_name] = config_type(config_value)

        # create inputs for the widget config
        dpg.add_separator(parent=self.inputs_group, label='Widget config')
        for name, value in deepcopy(self.active_widget.config).items():
            self.get_input(name, value, self.active_widget.config_definition[name], update_widget_config)

        dpg.add_separator(parent=self.inputs_group)

        dpg.add_button(parent=self.inputs_group, label='Save', callback=self.save_config, width=-1)

    def get_input(self, name: str, value: any, config_item: Types.Base, callback: callable, parent: int = None):
        """ creates an input depending on the value's type """
        item_config = dict(  # common config for all inputs
            parent=parent if parent is not None else self.inputs_group,
            label=name,
            default_value=value,
            callback=callback,
            user_data=name
        )
        match type(config_item).__name__:  # depending on the type of this config item
            case 'Text':
                dpg.add_text(name, parent=item_config['parent'])
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
                subitem_type: Types.Base = config_item.config
                list_group = dpg.add_tree_node(label=name, parent=item_config['parent'], default_open=True)
                def build_ui():
                    dpg.delete_item(list_group, children_only=True)  # clear all previous elements
                    for i, item_value in enumerate(value):  # create new ones
                        def list_callback(_, new_item_value, index):
                            # update the value list and call the callback
                            value[int(index)] = new_item_value
                            callback(None, value, name)
                        item_group = dpg.add_group(parent=list_group, horizontal=True)
                        self.get_input(str(i), item_value, subitem_type, list_callback, item_group)

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
                dpg.add_button(label=f'Add to {name}', width=-1, callback=add_item_callback, parent=item_config['parent'])

            case 'Group':
                subitems: dict[str, Types.Base] = config_item.config
                item_group = dpg.add_tree_node(label=name, parent=item_config['parent'], default_open=True)
                for item_name, item_type in subitems.items():
                    item_value = value[item_name]
                    def list_callback(_, new_item_value, item_name):
                        # update the value list and call the callback
                        value[item_name] = new_item_value
                        callback(None, value, name)
                    self.get_input(item_name, item_value, item_type, list_callback, item_group)



    def save_config(self):
        """ destroy and re-create the selected widget with the new config """
        if self.active_widget is not None:
            old_widget_config = self.active_widget.config
            old_window_config = self.active_widget.window_config
            window_tag = self.active_widget.window  # keep the same window tag
            new_widget = type(self.active_widget)(  # create a new widget
                {**old_window_config, **self.new_window_config},  # merge old config with the new config
                {**old_widget_config, **self.new_widget_config},
                window_tag
            )
            new_widget.ready = True  # set widget ready only after __init__ is done

    def render(self):
        # udate the active widget
        active_window = dpg.get_active_window()
        if active_window == self.window:  # abort if the selected window is the widget config window
            return

        widget = get_widget(active_window)
        if widget:  # selected window is a widget
            if self.active_widget == widget:  # abort if the selected widget has not changed
                return
            # different widget selected
            self.new_widget_config = {}
            self.new_window_config = {}
            self.active_widget = widget
            self.render_config_window()

        if not widget and self.active_widget is not None:  # selected window is not a widget
            self.active_widget = None
            dpg.delete_item(self.inputs_group, children_only=True)
