import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget, WidgetConfigItem, WidgetConfigGroup
from plugins.data_store import DataStore
from plugins.widget_config import DataPoint


class StatusTableWidget(BaseWidget):
    name = 'Status table'

    config_definition = {
        'test': WidgetConfigItem(list[WidgetConfigItem(int)]),
        'test2': WidgetConfigItem(list[WidgetConfigItem(DataPoint)]),
        'test3': WidgetConfigItem(WidgetConfigGroup[{
            'ok': WidgetConfigItem(str, 'test'),
            'ok2': WidgetConfigItem(int)
        }]),
        'rfgefgr': WidgetConfigItem(list[
            WidgetConfigItem(WidgetConfigGroup[{
                'ok': WidgetConfigItem(DataPoint),
                'ok2': WidgetConfigItem(int)
            }])
        ]),
    }

    def __init__(self, *args):
        super(StatusTableWidget, self).__init__(*args)
        print(self.config)

        for k in self.config.keys():
            dpg.add_text(str(k), parent=self.window)
            for v in self.config[k]:
                dpg.add_text(f'  {v}', parent=self.window)

    def render(self):
        pass