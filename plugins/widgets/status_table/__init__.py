import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data


class StatusTableWidget(BaseWidget):
    name = 'Status table'

    config_definition = {
        '"expression" is python code': config_types.Text(),
        'Call red() yellow() green() gray() or color(r,g,b) to set the cell color': config_types.Text(),
        'The "data" dict is available to access data values': config_types.Text(),
        'items': config_types.List(config_types.Group({
                'expression': config_types.Str({'multiline': True}),
                'x': config_types.Int(),
                'y': config_types.Int(),
                'label': config_types.Str()
            })
        ),
    }

    def __init__(self, *args):
        super().__init__(*args)
        if len(self.config['items']) == 0:
            return
        cols = max(item['x'] for item in self.config['items'])+1
        rows = max(item['y'] for item in self.config['items'])+1
        self.cells: list[list[int]] = []
        self.texts = {}
        self.code = {}

        with dpg.theme() as container_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
            dpg.bind_item_theme(self.window, container_theme)

        with dpg.table(parent=self.window, header_row=False, borders_innerV=True, borders_innerH=True) as self.table:
            for i in range(cols):
                dpg.add_table_column()
            for i in range(rows):
                self.cells.append([])
                with dpg.table_row():
                    for j in range(cols):
                        self.cells[i].append(dpg.add_table_cell())
            for i, item in enumerate(self.config['items']):
                self.texts[i] = dpg.add_button(label=item['label'], parent=self.cells[item['y']][item['x']], enabled=False, width=-1)
                self.code[i] = compile(item['expression'], f'status x:{item['x']} y:{item['y']}', 'exec')

        with dpg.theme() as container_theme:
            with dpg.theme_component(dpg.mvTable):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0, 0))
            dpg.bind_item_theme(self.table, container_theme)

    def render(self):
        for i, item in enumerate(self.config['items']):
            def color_cell(r: int, g: int, b: int):
                dpg.highlight_table_cell(self.table, item['y'], item['x'], [r, g, b, 100])
            def set_text(text: str):
                dpg.set_value(self.texts[i], text)

            exec_locals = {
                'red': lambda: color_cell(255, 0, 0),
                'green': lambda: color_cell(0, 255, 0),
                'yellow': lambda: color_cell(255, 200, 0),
                'gray': lambda: color_cell(150, 150, 150),
                'text': set_text,
                'color': color_cell,
                'data': Data.plugin.data
            }
            exec(self.code[i], locals=exec_locals)