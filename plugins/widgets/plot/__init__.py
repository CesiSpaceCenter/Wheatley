import bisect

import dearpygui.dearpygui as dpg
import math

from plugins.base_widget import BaseWidget, Types
from plugins.data import Data


class PlotWidget(BaseWidget):
    name = 'Plot'

    config_definition = {
        'series': Types.List(Types.Group({
            'x': Types.DataPoint(),
            'y': Types.DataPoint()
        }))
    }

    reload = False

    def __init__(self, *args):
        super(PlotWidget, self).__init__(*args)

        with dpg.theme() as container_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
            dpg.bind_item_theme(self.window, container_theme)


        self.plot = dpg.add_plot(parent=self.window, width=-1, height=-1, no_mouse_pos=True)
        dpg.add_plot_legend(parent=self.plot)

        # horizontal axis
        self.x_axis = dpg.add_plot_axis(axis=dpg.mvXAxis, parent=self.plot)

        self.series = {}  # dict that will store every dpg's Series
        self.tooltip = None  # dpg tooltip that display the point coordinates near the mouse
        self.y_axis = {}  # dict that will store every dpg's YAxis

        # create the axis
        for ser in self.config['series']:
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

        with dpg.custom_series([], [], channel_count=2, parent=self.x_axis, callback=self.mouse_event):
            self.tooltip = dpg.add_text()
        self.reload = True

    last_mouse_x = 0
    def mouse_event(self, _, mouse):
        px = mouse[0]['MouseX_PlotSpace']
        if math.isinf(px):
            return
        if px == self.last_mouse_x:
            return
        self.last_mouse_x = px
        texts = []
        for ser in self.config['series']:
            if ser['y'] not in self.series:
                continue
            data_x = Data.plugin.data[ser['x']]
            data_y = Data.plugin.data[ser['y']]
            i = bisect.bisect_left(data_x, px)
            if i >= len(data_x):
                i = len(data_x) - 1
            elif i and data_x[i] - px > px - data_x[i - 1]:
                i = i - 1
            try:
                data_y[i]
            except IndexError:
                print(i, px, len(data_x))
            texts.append(f'{ser["y"]} {round(data_x[i], 2)}, {round(data_y[i], 2)}')
        dpg.set_value(self.tooltip, '\n'.join(texts))

    def render(self):
        if not Data.plugin.has_changed and not self.reload:
            return

        # get the datapoit's data from the datastore
        data = Data.plugin.data
        if self.config['series'] == '':  # ignore if no datapoint has been configured
            return

        Data.plugin.has_changed = False
        self.reload = False

        # update the axis limits to fit with new the data
        #dpg.set_axis_limits(self.x_axis, data_x[0] - 30, data_x[-1])
        for ser in self.config['series']:
            if len(data[ser['x']]) == 0 or len(data[ser['x']]) == 0:  # ignore if there is no data yet
                continue

            data_x = data[ser['x']]
            data_y = data[ser['y']]
            print(dpg.get_item_theme(self.series[ser['y']]))

            dpg.set_value(self.series[ser['y']], [data_x, data_y])  # update the series with the new x and y data
