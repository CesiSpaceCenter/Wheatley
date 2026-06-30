import dearpygui.dearpygui as dpg
import math

from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data


class PlotWidget(BaseWidget):
    name = 'Plot'

    config_definition = {
        'series': config_types.List(config_types.DataPoint())
    }

    def __init__(self, *args):
        super().__init__(*args)

        with dpg.theme() as container_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
            dpg.bind_item_theme(self.window, container_theme)


        self.plot = dpg.add_plot(parent=self.window, width=-1, height=-1, no_mouse_pos=True, crosshairs=True)
        dpg.add_plot_legend(parent=self.plot)

        # horizontal axis
        self.x_axis_relative = dpg.add_plot_axis(axis=dpg.mvXAxis2, parent=self.plot, no_gridlines=True)
        self.x_axis = dpg.add_plot_axis(axis=dpg.mvXAxis, parent=self.plot, no_tick_labels=True)

        self.series = {}  # dict that will store every dpg's Series
        self.tags = {}  # dpg tooltip that display the point coordinates near the mouse
        self.y_axis = {}  # dict that will store every dpg's YAxis

        # create the axis
        for data_point_name in self.config['series']:
            if data_point_name == '':
                continue

            data_point = Data.plugin.dictionary[data_point_name]  # get the datapoint config from the datastore

            # each axis represent a unit if available, or a datapoint
            axis_name = data_point.unit if data_point.unit != '' else data_point.name

            if axis_name not in self.y_axis:
                # dpg limits to 3 y axis, so choose between mvYAxis, mvYAxis2, mvYAxis3
                if len(self.y_axis) > 2:
                    raise Exception('Reached limit of 3 y axis')
                axis = [dpg.mvYAxis, dpg.mvYAxis2, dpg.mvYAxis3][len(self.y_axis)]
                # create the y_axis
                self.y_axis[axis_name] = dpg.add_plot_axis(axis=axis, parent=self.plot, label=axis_name)

            # create the series
            self.series[data_point_name] = dpg.add_line_series(
                parent=self.y_axis[axis_name],
                label=data_point.name + (f' ({data_point.unit})' if data_point.unit else ''),
                x=[],
                y=[]
            )

    def render(self):
        if self.config['series'] == '':  # ignore if no datapoint has been configured
            return

        #Data.plugin.has_changed = False ############## AAAAAAAAAAAAAAAAAAAAAH C4EST CA QUI PUE LA MERDE

        # update the axis limits to fit with new the data
        min_x = math.nan
        max_x = math.nan
        min_y = {}
        max_y = {}
        for data_point_name in self.config['series']:
            data_point = Data.plugin.dictionary[data_point_name]
            if not data_point.has_data:
                continue
            data = data_point[:]
            data_x = [p[0] for p in data]
            data_y = [p[1] for p in data]

            if math.isnan(min_x) or min_x > min(data_x):
                min_x = min(data_x)
            if math.isnan(max_x) or max_x < max(data_x):
                max_x = max(data_x)

            if data_point_name not in min_y or min_y[data_point_name] > data_point.min:
                min_y[data_point_name] = data_point.min

            if data_point_name not in max_y or max_y[data_point_name] > data_point.max:
                max_y[data_point_name] = data_point.max

            dpg.set_value(self.series[data_point_name], [data_x, data_y])  # update the series with the new x and y data

        dpg.set_axis_limits(self.x_axis, min_x, max_x)
        dpg.set_axis_limits(self.x_axis_relative, min_x-max_x, 0)
        for axis_name, axis in self.y_axis.items():
            margin = (max_y[axis_name] - min_y[axis_name]) * 0.1
            if margin == 0:
                margin = 1
            dpg.set_axis_limits(axis, min_y[axis_name]-margin, max_y[axis_name]+margin)