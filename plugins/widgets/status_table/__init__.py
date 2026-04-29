import dearpygui.dearpygui as dpg
from math import ceil

from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types


class StatusTableWidget(BaseWidget):
    name = 'Status table'

    config_definition = {
        '"expression" is a piece of python code that should define a variable "color"': config_types.Text(),
        'The "color" variable should have values gray, green, yellow, red': config_types.Text(),
        'The "data" dict is available to access data values': config_types.Text(),
        'items': config_types.List(config_types.Group({
                'expression': config_types.Str({'multiline': True}),
                'x': config_types.Int(),
                'y': config_types.Int(),
                'label': config_types.Str()
            })
        ),
    }

    colors = {}

    def __init__(self, *args):
        super(StatusTableWidget, self).__init__(*args)
        if len(self.config['items']) == 0:
            return

        for color_name, color in {
            'gray': (150, 150, 150),
            'green': (50, 160, 50),
            'yellow': (150, 150, 0),
            'red': (200, 0, 0)
        }.items():
            with dpg.theme() as theme:
                self.colors[color_name] = theme
                with dpg.theme_component(dpg.mvButton):
                    dpg.add_theme_color(dpg.mvThemeCol_Button, color)
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, color)


        cols = max(item['x'] for item in self.config['items'])+1
        rows = max(item['y'] for item in self.config['items'])+1
        print(rows, cols)

        cells: list[list[int]] = []

        with dpg.table(parent=self.window, header_row=False) as self.table:
            with dpg.theme() as tight_table_theme:
                with dpg.theme_component(dpg.mvTable):
                    dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 1, 1, category=dpg.mvThemeCat_Core)
                    dpg.bind_item_theme(self.table, tight_table_theme)
            for i in range(cols):
                dpg.add_table_column()
            for i in range(rows):
                cells.append([])
                with dpg.table_row():
                    for j in range(cols):
                        cells[i].append(dpg.add_table_cell())
                        print(j,i)
            for i, item in enumerate(self.config['items']):
                item['compiled_expr'] = compile(item['expression'], item['label'], 'exec')
                item['button'] = dpg.add_button(label=item['label'], parent=cells[item['y']][item['x']], width=-1)

    def render(self):
        for i, item in enumerate(self.config['items']):
            context = {'color': 'gray'}
            try:
                exec(item['compiled_expr'], {}, context)
            except Exception as e:
                context['color'] = 'gray'
            #dpg.highlight_table_cell(self.table, item['y'], item['x'], [*self.colors[e], 100])
            dpg.bind_item_theme(item['button'], self.colors[context['color']])