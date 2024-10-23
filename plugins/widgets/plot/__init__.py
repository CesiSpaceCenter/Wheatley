import time
import math

import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget


class PlotWidget(BaseWidget):
    default_config = {
        'y_axis': [
            'temp'
        ],
        'series': [
            {
                'name': 'temperature moteur',
                'axis': 'temp'
            }
        ]
    }

    default_window_config = {
    }

    y_axis = {}

    series = {}

    data = {}
    data_x = []

    def __init__(self, window_config=None, widget_config=None):
        super(PlotWidget, self).__init__(window_config, widget_config)
        self.plot = dpg.add_plot(parent=self.window, width=-1, height=-1)
        dpg.add_plot_legend(parent=self.plot)
        for ax in self.config['y_axis']:
            self.y_axis[ax] = dpg.add_plot_axis(axis=dpg.mvYAxis, parent=self.plot, label=ax)
        self.x_axis = dpg.add_plot_axis(axis=dpg.mvXAxis, parent=self.plot, label='t')
        for ser in self.config['series']:
            self.series[ser['name']] = dpg.add_line_series(parent=self.y_axis[ser['axis']], label=ser['name'], x=[], y=[])
            self.data[ser['name']] = []
        self._update()

    def _update(self):
        self.data_x.append(time.monotonic())
        dpg.set_axis_limits(self.x_axis, self.data_x[-1]-30, self.data_x[-1])
        for series_name, ser in self.series.items():
            self.data[series_name].append(math.sin(self.data_x[-1]))
            dpg.set_value(ser, [self.data_x, self.data[series_name]])

    def render(self):
        self._update()
