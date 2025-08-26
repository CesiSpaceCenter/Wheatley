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

    reload = False

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

        dpg.add_custom_series([], [], channel_count=1, parent=self.x_axis, callback=self.mouse_event, show=True, no_fit=True)

        self.series = {}  # dict that will store every dpg's Series
        self.tags = {}  # dpg tooltip that display the point coordinates near the mouse
        self.y_axis = {}  # dict that will store every dpg's YAxis

        # create the axis
        for ser in self.config['series']:
            print('creating series', ser)
            if ser['x'] == '' or ser['y'] == '':
                continue

            data_point = Data.plugin.dictionary[ser['y']]  # get the datapoint config from the datastore

            # every y axis represents a unit
            if data_point.unit not in self.y_axis:
                # dpg limits to 3 y axis, so choose between mvYAxis, mvYAxis2, mvYAxis3
                if len(self.y_axis) > 2:
                    raise Exception('Reached limit of 3 y axis')
                axis = [dpg.mvYAxis, dpg.mvYAxis2, dpg.mvYAxis3][len(self.y_axis)]
                # create the y_axis
                self.y_axis[data_point.unit] = dpg.add_plot_axis(axis=axis, parent=self.plot, label=data_point.unit)

            # create the series
            self.series[ser['y']] = dpg.add_line_series(
                parent=self.y_axis[data_point.unit],
                label=data_point.name + (f' ({data_point.unit})' if data_point.unit else ''),
                x=[],
                y=[]
            )
            print('created series', ser)

        self.reload = True
        print('init done')

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

            #print('mouse move', self.mouse_x)
            for ser in self.config['series']:
                if ser['y'] == '' or ser['x'] == '' or ser['y'] not in self.config['series']:
                    continue
                data_x = Data.plugin.data[ser['x']]
                data_y = Data.plugin.data[ser['y']]
                if len(data_x) != len(data_y):
                    print('XY sizes mismatch for', ser['y'])
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

        if not Data.plugin.has_changed and not self.reload:
            return
        print('render')

        # get the datapoit's data from the datastore
        data = Data.plugin.data
        if self.config['series'] == '':  # ignore if no datapoint has been configured
            return

        Data.plugin.has_changed = False
        self.reload = False

        # update the axis limits to fit with new the data
        #dpg.set_axis_limits(self.x_axis, data_x[0] - 30, data_x[-1])
        print('populating series')
        for ser in self.config['series']:
            data_x = data[ser['x']]
            data_y = data[ser['y']]
            if len(data_x) == 0 or len(data_y) == 0:  # ignore if there is no data yet
                continue
            if len(data_x) != len(data_y):
                print('XY sizes mismatch for', ser['y'])
                return

            print(len(data_x), len(data_y))

            dpg.set_value(self.series[ser['y']], [data_x, data_y])  # update the series with the new x and y data
