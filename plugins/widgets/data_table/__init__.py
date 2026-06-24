import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.data import Data


class DataTableWidget(BaseWidget):
    name = 'Data table'

    def __init__(self, *args):
        super().__init__(*args)

        self.plots = []

        with dpg.theme() as container_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 3)
            dpg.bind_item_theme(self.window, container_theme)

        def search_callback(_, query):
            dpg.set_value(self.table, query)
        dpg.add_input_text(label='Search', callback=search_callback, parent=self.window, width=100)

        self.rows = {}

        with dpg.table(parent=self.window,  resizable=True, borders_innerH=True) as self.table:
            dpg.add_table_column(label='Key')
            dpg.add_table_column(label='Value')
            dpg.add_table_column(label='Unit')
            dpg.add_table_column(label='Plot')

            for item in Data.plugin.dictionary.values():
                with dpg.table_row(filter_key=item.name):
                    self.rows[item.name] = {}
                    with dpg.table_cell():
                        dpg.add_text(item.name)
                    with dpg.table_cell():
                        dpg.add_text(item.unit)
                    with dpg.table_cell():
                        self.rows[item.name]['value'] = dpg.add_text()
                    with dpg.table_cell():
                        self.rows[item.name]['plot'] = dpg.add_simple_plot(width=-1)

    def render(self):
        for key, row in self.rows.items():
            dpg.set_value(row['value'], round(Data.plugin.data[key][-1], 2))
            dpg.set_value(row['plot'], Data.plugin.data[key])

