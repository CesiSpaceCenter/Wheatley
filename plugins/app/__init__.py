import os

import dearpygui.dearpygui as dpg
import easygui
import json

import base_app
from plugins.base_plugin import BasePlugin

from plugins.loading import Loading

from plugins.widgets.text import TextWidget
from plugins.widgets.plot import PlotWidget
from plugins.widgets.numeric import NumericWidget
from plugins.widgets.numeric_bar import NumericBarWidget
from utils import get_widget

# the "app" is the layout configuration created by the user
# this plugin is responsible for loading an app file (creating all of the correspondig widgets)
# and saving an app file (listing all of the widgets)


class App(BasePlugin):
    current_file = None
    widgets = [
        ('text', TextWidget),
        ('plot', PlotWidget),
        ('numeric bar', NumericBarWidget),
        ('numeric', NumericWidget)
    ]

    def __init__(self):
        dpg.configure_app(docking=True, docking_space=True)
        with dpg.menu(parent='menubar', label='App'):
            dpg.add_menu_item(label='Open an app file', callback=self.open_file_dialog)
            dpg.add_menu_item(label='Save', callback=lambda: self._save())
            dpg.add_menu_item(label='Save as', callback=self.save_file_dialog)
            with dpg.menu(label='Add widget'):
                new_widget_type = dpg.add_listbox(items=[w[0] for w in self.widgets], num_items=len(self.widgets))
                def add_widget_callback():
                    widget_type = dpg.get_value(new_widget_type)
                    for widget in self.widgets:
                        if widget[0] == widget_type:
                            widget_object = widget[1]()
                            widget_object.ready = True
                            break
                dpg.add_button(label='Add', width=-1, callback=add_widget_callback)

        if 'APP_FILE' in os.environ:
            self._load(os.environ['APP_FILE'])

    def open_file_dialog(self):
        path = easygui.fileopenbox(filetypes=['*.json'])
        if path is not None and path != '':
            os.environ['APP_FILE'] = path
            base_app.should_restart = True

    def save_file_dialog(self):
        Loading.plugin.open()
        path = easygui.filesavebox(filetypes=['*.json'])
        if path is not None and path != '':
            self._save(path)
        Loading.plugin.close()

    def _load(self, path: str):
        self.current_file = path

        dpg.configure_app(docking=True, docking_space=True, init_file=path+'.ini')
        with open(path, 'r') as f:
            data = json.loads(f.read())
            for widget_data in data['widgets']:
                for widget in self.widgets:
                    if widget[0] == widget_data['widget']:
                        widget_object = widget[1](None, widget_data['config'], widget_data['window_tag'])
                        widget_object.ready = True
                        break

    def _save(self, path: str = None):
        if path is None:
            if self.current_file is None:
                self.save_file_dialog()
                return
            path = self.current_file
        data = {
            'widgets': []
        }
        for item in dpg.get_all_items():
            widget = get_widget(item)
            if widget:
                widget_type = None
                for w in self.widgets:
                    if w[1] == type(widget):
                        widget_type = w[0]
                        break

                data['widgets'].append({
                    'window_tag': widget.window,
                    'widget': widget_type,
                    'config': widget.config,
                    'window': widget.window_config
                })
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=2))

        dpg.save_init_file(path + '.ini')

    def render(self):
        for window in dpg.get_all_items():
            widget = get_widget(window)
            if widget and widget.ready:
                widget.render()
