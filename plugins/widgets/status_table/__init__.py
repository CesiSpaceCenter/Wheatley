import dearpygui.dearpygui as dpg
from math import ceil

from plugins.base_widget import BaseWidget, WidgetConfigItem, WidgetConfigGroup
from plugins.widget_config import WidgetConfigText, long_str


class StatusTableWidget(BaseWidget):
    name = 'Status table'

    config_definition = {
        'cols': WidgetConfigItem(int, 3),
        '"expression" is a piece of python code that should return 0=Gray, 1=Green, 2=Yellow, 3=Red': WidgetConfigItem(WidgetConfigText),
        'The "data" dict is available to access data values': WidgetConfigItem(WidgetConfigText),
        'items': WidgetConfigItem(list[
            WidgetConfigItem(WidgetConfigGroup[{
                'expression': WidgetConfigItem(long_str),
                'label': WidgetConfigItem(str)
            }])
        ]),
    }

    colors = [
        (255, 0, 0),
        (255, 255, 0),
        (255, 130, 130),
        (255, 0, 255),
        (130, 0, 0),
        (0, 0, 255),
        (255, 200, 200),
        (0, 130, 130),
    ]

    def __init__(self, *args):
        super(StatusTableWidget, self).__init__(*args)
        rows = ceil(len(self.config['items'])/self.config['cols'])
        print(rows, self.config['cols'])

        with dpg.table(parent=self.window, header_row=False, borders_innerV=True, borders_innerH=True) as table:
            for i in range(self.config['cols']):
                dpg.add_table_column()
            index = 0
            for i in range(rows):
                with dpg.table_row():
                    for j in range(self.config['cols']):
                        with dpg.table_cell():
                            if index < len(self.config['items']):
                                dpg.highlight_table_cell(table, i, j, [*self.colors[index], 100])
                                dpg.add_text(self.config['items'][index]['label'])
                                index += 1


    def render(self):
        pass