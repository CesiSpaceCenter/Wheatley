import dearpygui.dearpygui as dpg
import json

from plugins.base_plugin import BasePlugin
from plugins.base_widget import BaseWidget
from plugins.text_widget import TextWidget

# the "app" is the layout configuration created by the user
# this plugin is responsible for loading an app file (creating all of the correspondig widgets)
# and saving an app file (listing all of the widgets)


class App(BasePlugin):
    current_app_file = None
    widgets: dict[str, BaseWidget] = {
        'text': TextWidget
    }

    def __init__(self):
        with dpg.file_dialog(
            show=False,
            callback=self._open_app_file,
            tag='app_file_dialog',
            file_count=1,
            modal=True,
            width=600,
            height=400
        ):
            dpg.add_file_extension('.json')
        with dpg.menu(parent='menubar', label='App'):
            dpg.add_menu_item(label='Open an app file', callback=lambda: dpg.show_item('app_file_dialog'))
            with dpg.menu(label='Add widget'):
                def add_widget_callback():
                    widget_type = dpg.get_value('new_widget_type')
                    self.widgets[widget_type]()
                dpg.add_listbox(tag='new_widget_type', items=list(self.widgets), num_items=len(self.widgets))
                dpg.add_button(label='Add', width=-1, callback=add_widget_callback)

    def _open_app_file(self, _sender, files):
        self._load(list(files['selections'].values())[0])

    def _load(self, path: str):
        print('loading', path)
        self.current_app_file = path
        with open(path, 'r') as f:
            data = json.loads(f.read())
            for widget_data in data['widgets']:
                widget = self.widgets[widget_data['widget']](widget_data['window'], widget_data['config'])
