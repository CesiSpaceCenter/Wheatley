import os

import dearpygui.dearpygui as dpg
import easygui
import json

import base_app
from plugins.base_plugin import BasePlugin
from plugins.base_widget import BaseWidget

from plugins.loading import Loading

from plugins.widgets.text import TextWidget
from plugins.widgets.plot import PlotWidget
from plugins.widgets.numeric import NumericWidget
from plugins.widgets.numeric_bar import NumericBarWidget
from utils import get_widget

# the "app" is the layout configuration created by the user
# this plugin is responsible for loading an app file (creating all of the coresponding widgets)
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
        with dpg.menu(parent='menubar', label='App'):  # add an "App" menu to the menubar
            dpg.add_menu_item(label='Open an app file', callback=self.open_file_dialog)
            dpg.add_menu_item(label='Save', callback=self.save)
            dpg.add_menu_item(label='Save as', callback=self.save_file_dialog)
            with dpg.menu(label='Add widget'):
                def add_widget_callback(_sender, _, widget: BaseWidget):
                    widget_object = widget()
                    widget_object.ready = True  # set ready only after __init__ is done
                for widget in self.widgets:  # add a menu item for each widget
                    dpg.add_menu_item(label=widget[0], callback=add_widget_callback, user_data=widget[1])

        if 'APP_FILE' in os.environ:  # open app file if there is one in the env var
            self.load(os.environ['APP_FILE'])

    @staticmethod
    def open_file_dialog():
        """ Opens a dialog to open and load an app file """
        path = easygui.fileopenbox(filetypes=['*.json'])  # TODO: replace easygui, sometimes crashes
        if path is not None and path != '':
            # we have to restart the whole app, since dearpygui's init files only load on viewport creation
            os.environ['APP_FILE'] = path
            base_app.should_restart = True

    def save_file_dialog(self):
        """ Opens a dialog to save the current layout & config """
        Loading.plugin.open()
        path = easygui.filesavebox(filetypes=['*.json'])
        if path is not None and path != '':
            self.save(path)
        Loading.plugin.close()

    def load(self, path: str):
        """ Loads an app file, creating its widgets and configuration """
        self.current_file = path

        # load dearpygui's init file for the layout
        dpg.configure_app(docking=True, docking_space=True, init_file=path+'.ini')
        with open(path, 'r') as f:  # open the widgets file
            data = json.loads(f.read())
            for widget_data in data['widgets']:  # for every widget in the widgets file
                for widget in self.widgets:  # find the corresponding widget
                    if widget[0] == widget_data['widget']:  # corresponding name
                        # create the widget object from its class, with the widget&window config and the window tag.
                        widget_object: BaseWidget = widget[1](widget_data['window'], widget_data['config'], widget_data['window_tag'])
                        widget_object.ready = True  # only after __init__ is done, set the widget as ready
                        break

    def save(self, path: str = None):
        """ Saves an app file, with its widgets and configuration """
        # show the dialog if there is no path argument, and there is no opened app file to overwrite
        if path is None:
            if self.current_file is None:
                self.save_file_dialog()
                return
            path = self.current_file
        data = {  # save file content
            'widgets': []
        }
        # find all widgets
        for item in dpg.get_all_items():
            widget = get_widget(item)
            if widget:
                widget_type = None
                # find the widget type name
                for w in self.widgets:
                    if w[1] == type(widget):
                        widget_type = w[0]
                        break

                # add the widget to the config
                data['widgets'].append({
                    'window_tag': widget.window,
                    'widget': widget_type,
                    'config': widget.config,
                    'window': widget.window_config
                })
        # save the save file
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=2))

        # save the init file
        dpg.save_init_file(path + '.ini')

    def render(self):
        # call the render method for all widgets
        for window in dpg.get_all_items():
            widget = get_widget(window)
            if widget and widget.ready:
                widget.render()
