import dearpygui.dearpygui as dpg
import easygui
import json

from plugins.base_plugin import BasePlugin
from plugins.base_widget import BaseWidget

from plugins.loading import Loading

from plugins.widgets.text import TextWidget
from plugins.widgets.plot import PlotWidget
from plugins.widgets.numeric import NumericWidget
from utils import get_widget

# the "app" is the layout configuration created by the user
# this plugin is responsible for loading an app file (creating all of the correspondig widgets)
# and saving an app file (listing all of the widgets)


class App(BasePlugin):
    current_file = None
    widgets = [
        ('text', TextWidget),
        ('plot', PlotWidget),
        ('numeric', NumericWidget)
    ]

    def __init__(self):
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
                            widget[1]()
                            break
                dpg.add_button(label='Add', width=-1, callback=add_widget_callback)

    def open_file_dialog(self):
        Loading.plugin.open()
        path = easygui.fileopenbox(filetypes=['*.json'])
        if path is not None and path != '':
            self._load(path)
        Loading.plugin.close()

    def save_file_dialog(self):
        Loading.plugin.open()
        path = easygui.filesavebox(filetypes=['*.json'])
        if path is not None and path != '':
            self._save(path)
        Loading.plugin.close()

    def _load(self, path: str):
        self.current_file = path
        with open(path, 'r') as f:
            data = json.loads(f.read())
            for widget_data in data['widgets']:
                for widget in self.widgets:
                    if widget[0] == widget_data['widget']:
                        widget[1](widget_data['window'], widget_data['config'])
                        break

    def _save(self, path: str = None):
        if path is None:
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
                    'widget': widget_type,
                    'config': widget.config,
                    'window': widget.window_config
                })
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=2))


    def render(self):
        for window in dpg.get_all_items():
            widget = get_widget(window)
            if widget and hasattr(widget, 'render'):
                widget.render()
