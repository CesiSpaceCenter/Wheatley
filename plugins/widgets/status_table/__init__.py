import dearpygui.dearpygui as dpg
from math import ceil

from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types


class StatusTableWidget(BaseWidget):
    name = 'Status table'

    config_definition = {
        '"expression" is a piece of python code that should return 0=Gray, 1=Green, 2=Yellow, 3=Red': config_types.Text(),
        'The "data" dict is available to access data values': config_types.Text(),
        'items': config_types.List(config_types.Group({
                'expression': config_types.Str({'multiline': True}),
                'x': config_types.Int(),
                'y': config_types.Int(),
                'label': config_types.Str()
            })
        ),
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
        if len(self.config['items']) == 0:
            return
        cols = max(item['x'] for item in self.config['items'])+1
        rows = max(item['y'] for item in self.config['items'])+1
        print(rows, cols)

        cells = []

        with dpg.table(parent=self.window, header_row=False, borders_innerV=True, borders_innerH=True) as table:
            for i in range(cols):
                dpg.add_table_column()
            for i in range(rows):
                cells.append([])
                with dpg.table_row():
                    for j in range(cols):
                        cells[i].append(dpg.add_table_cell())
            for i, item in enumerate(self.config['items']):
                dpg.highlight_table_cell(table, item['y'], item['x'], [*self.colors[i], 100])
                dpg.add_text(item['label'], parent=cells[item['y']][item['x']])


    def render(self):
        pass