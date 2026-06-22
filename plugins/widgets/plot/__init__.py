import bisect

import dearpygui.dearpygui as dpg
import math

from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data


class PlotWidget(BaseWidget):
    name = 'Plot'

    config_definition = {
        'series': config_types.List(config_types.Group({
            'x': config_types.DataPoint(),
            'y': config_types.DataPoint()
        }))
    }

    def __init__(self, *args):
        super(PlotWidget, self).__init__(*args)

        with dpg.theme() as container_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
            dpg.bind_item_theme(self.window, container_theme)


        self.plot = dpg.add_plot(parent=self.window, width=-1, height=-1, no_mouse_pos=True, crosshairs=True)
        dpg.add_plot_legend(parent=self.plot)

        # horizontal axis
        self.x_axis = dpg.add_plot_axis(axis=dpg.mvXAxis, parent=self.plot)

        #dpg.add_custom_series([], [], channel_count=1, parent=self.x_axis, callback=self.mouse_event, show=True, no_fit=True)

        self.series = {}  # dict that will store every dpg's Series
        self.tags = {}  # dpg tooltip that display the point coordinates near the mouse
        self.y_axis = {}  # dict that will store every dpg's YAxis

        # create the axis
        for ser in self.config['series']:
            if ser['x'] == '' or ser['y'] == '':
                continue

            data_point = Data.plugin.dictionary[ser['y']]  # get the datapoint config from the datastore

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
            self.series[ser['y']] = dpg.add_line_series(
                parent=self.y_axis[axis_name],
                label=data_point.name + (f' ({data_point.unit})' if data_point.unit else ''),
                x=[],
                y=[]
            )

    last_mouse_x = 0
    mouse_x = 0
    def mouse_event(self, _, mouse):
        self.mouse_x = mouse[0]['MouseX_PlotSpace']

    def render(self):
        if self.ready and self.mouse_x != self.last_mouse_x:
            self.last_mouse_x = self.mouse_x
            x_min, x_max = dpg.get_axis_limits(self.x_axis)
            if math.isinf(self.mouse_x) or int(self.mouse_x) not in range(int(x_min), int(x_max)):  # mouse is out of the plot
                self.mouse_x = -1

            for ser in self.config['series']:
                if ser['y'] == '' or ser['x'] == '' or ser['y'] not in self.config['series']:
                    continue
                data_x = Data.plugin.data[ser['x']]
                data_y = Data.plugin.data[ser['y']]
                if len(data_x) != len(data_y):
                    self.logger.error(f'XY sizes mismatch for {ser['y']}')
                    continue
                data_point = Data.plugin.dictionary[ser['y']]
                if self.mouse_x != -1:
                    i = bisect.bisect_left(data_x, self.mouse_x)
                    if i >= len(data_x):
                        i = len(data_x) - 1
                    elif i and data_x[i] - self.mouse_x > self.mouse_x - data_x[i - 1]:
                        i = i - 1
                    dpg.configure_item(self.series[ser['y']], label=f'{data_point.name} ({data_y[i]}' + (data_point.unit if data_point.unit else '') + ')')
                else:
                    dpg.configure_item(self.series[ser['y']], label=data_point.name + (f' ({data_point.unit})' if data_point.unit else ''))


        # get the datapoit's data from the datastore
        data = Data.plugin.data
        if self.config['series'] == '':  # ignore if no datapoint has been configured
            return

        #Data.plugin.has_changed = False ############## AAAAAAAAAAAAAAAAAAAAAH C4EST CA QUI PUE LA MERDE

        # update the axis limits to fit with new the data
        min_x = 0
        max_x = 0
        min_y = {k: None for k in self.y_axis.keys()}
        max_y = {k: None for k in self.y_axis.keys()}
        for ser in self.config['series']:
            data_x = data[ser['x']]
            data_y = data[ser['y']]
            if len(data_x) == 0 or len(data_y) == 0:  # ignore if there is no data yet
                continue
            if len(data_x) != len(data_y):
                self.logger.error(f'XY sizes mismatch for {ser['y']} (x:{len(data_x)} y:{len(data_y)})')
                data_y = data_y[-len(data_x):]

            min_x = data_x[0]

            max_x = data_x[-1]

            if min_y[ser['y']] is None:
                min_y[ser['y']] = min(data_y)
            else:
                min_y[ser['y']] = min(min_y[ser['y']], min(data_y))

            if max_y[ser['y']] is None:
                max_y[ser['y']] = max(data_y)
            else:
                max_y[ser['y']] = max(max_y[ser['y']], max(data_y))

            dpg.set_value(self.series[ser['y']], [data_x, data_y])  # update the series with the new x and y data

        dpg.set_axis_limits(self.x_axis, min_x, max_x)
        for axis_name, axis in self.y_axis.items():
            margin = (max_y[axis_name] - min_y[axis_name]) * 0.1
            #if margin == 0:
            #    margin = 1
            dpg.set_axis_limits(axis, min_y[axis_name]-margin, max_y[axis_name]+margin)