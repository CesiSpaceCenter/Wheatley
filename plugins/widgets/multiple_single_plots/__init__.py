import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data


class MultipleSinglePlotsWidget(BaseWidget):
    name = 'Multiple single plots'

    config_definition = {
        'plot height': config_types.Int(default=150),
        'auto plot height': config_types.Bool(default=True),
        'series': config_types.List(config_types.DataPoint())
    }

    def __init__(self, *args):
        if type(self) == MultipleSinglePlotsWidget:  # don't init parent if MultipleSinglePlotsWidget is inherited (all_data_plots widget)
            super().__init__(*args)

        if not self.config['series']:
            return

        self.plots = []

        with dpg.theme() as container_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
            dpg.bind_item_theme(self.window, container_theme)

        if self.config['auto plot height']:
            subplot_height = (dpg.get_item_height(self.window) / len(self.config['series'])) * 0.95
        else:
            subplot_height = self.config['plot height']

        def search_callback(_, query):
            dpg.set_value(self.filter_set, query)
        dpg.add_input_text(label='Search', callback=search_callback, parent=self.window, width=100)

        with dpg.filter_set(parent=self.window) as self.filter_set:
            for i, data_point_name in enumerate(self.config['series']):
                data_point = Data.plugin.dictionary[data_point_name]

                plot = dpg.add_plot(parent=self.filter_set, width=-1, height=subplot_height, filter_key=data_point_name)

                x_axis_relative = dpg.add_plot_axis(axis=dpg.mvXAxis2, parent=plot, no_gridlines=True)
                x_axis = dpg.add_plot_axis(axis=dpg.mvXAxis, parent=plot, no_tick_labels=True)
                y_axis = dpg.add_plot_axis(axis=dpg.mvYAxis, parent=plot, label=data_point_name + (f' ({data_point.unit})' if data_point.unit else ''))

                series = dpg.add_line_series(
                    parent=y_axis,
                    x=[],
                    y=[]
                )

                self.plots.append({
                    'plot': plot,
                    'x_axis': x_axis,
                    'x_axis_relative': x_axis_relative,
                    'y_axis': y_axis,
                    'y': data_point_name,
                    'series': series
                })

    def render(self):
        if not self.config['series']:  # ignore if no datapoint has been configured
            return
        if not dpg.is_item_visible(self.window):
            return

        #Data.plugin.has_changed = False

        # update the axis limits to fit with new the data
        for plot in self.plots:
            data_point = Data.plugin.dictionary[plot['y']]
            if not data_point.has_data:  # ignore if there is no data yet
                continue

            data = data_point[:]
            data_x = [round(p[0], 2) for p in data]
            data_y = [p[1] for p in data]

            dpg.set_value(plot['series'], [data_x, data_y])  # update the series with the new x and y data


            # 10% margin on y-axis
            margin = (data_point.max - data_point.min) * 0.1
            if margin < 0.1:
                margin = 1

            dpg.set_axis_limits(plot['x_axis'], data_x[0], data_x[-1])
            dpg.set_axis_limits(plot['x_axis_relative'], data_x[0] - data_x[-1], 0)
            dpg.set_axis_limits(plot['y_axis'], data_point.min - margin, data_point.max + margin)
