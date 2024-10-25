import time
import math

import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget


class PlotWidget(BaseWidget):
    default_config = {
        'data': [
            {
                'name': 'temp',
                'unit': '°C'
            },
            {
                'name': 'temp mais un autre',
                'unit': '°C'
            },
            {
                'name': 'oula',
                'unit': 'feur'
            }
        ]
    }

    default_window_config = {
    }

    def __init__(self, window_config=None, widget_config=None):
        super(PlotWidget, self).__init__(window_config, widget_config)

        self.plot = dpg.add_plot(parent=self.window, width=-1, height=-1)
        dpg.add_plot_legend(parent=self.plot)

        self.x_axis = dpg.add_plot_axis(axis=dpg.mvXAxis, parent=self.plot, label='t')

        self.series = {}
        self.y_axis = {}
        self.data_y = {}
        self.data_x = []

        for data in self.config['data']:
            if data['unit'] not in self.y_axis:
                axis = [dpg.mvYAxis, dpg.mvYAxis2, dpg.mvYAxis3][len(self.y_axis)]
                self.y_axis[data['unit']] = dpg.add_plot_axis(axis=axis, parent=self.plot, label=data['unit'])

            self.series[data['name']] = dpg.add_line_series(parent=self.y_axis[data['unit']], label=data['name'], x=[], y=[])
            self.data_y[data['name']] = []
        self._update()

    def _update(self):
        if len(self.data_x) == 0:
            t = 1
        else:
            t = self.data_x[-1] + 1
        self.data_x.append(t)
        dpg.set_axis_limits(self.x_axis, self.data_x[-1]-30, self.data_x[-1])
        for i, (series_name, ser) in enumerate(self.series.items()):
            self.data_y[series_name].append(math.sin(time.monotonic()+i))
            dpg.set_value(ser, [self.data_x, self.data_y[series_name]])

    def render(self):
        self._update()
