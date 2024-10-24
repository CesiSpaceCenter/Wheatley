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
        ],
        'y_axis': {},
        'series': {},
        'data_y': {},
        'data_x': []
    }

    default_window_config = {
    }

    def __init__(self, window_config=None, widget_config=None):
        super(PlotWidget, self).__init__(window_config, widget_config)
        self.plot = dpg.add_plot(parent=self.window, width=-1, height=-1)
        dpg.add_plot_legend(parent=self.plot)

        for ax in self.config['y_axis']:
            self.config['y_axis'][ax] = dpg.add_plot_axis(axis=dpg.mvYAxis, parent=self.plot, label=ax)

        self.x_axis = dpg.add_plot_axis(axis=dpg.mvXAxis, parent=self.plot, label='t')

        for data in self.config['data']:
            if data['unit'] not in self.config['y_axis']:
                print('new axis', data['unit'])
                self.config['y_axis'][data['unit']] = dpg.add_plot_axis(axis=dpg.mvYAxis, parent=self.plot, label=data['unit'])

            print(data['name'], 'is on axis', self.config['y_axis'][data['unit']])
            self.config['series'][data['name']] = dpg.add_line_series(parent=self.config['y_axis'][data['unit']], label=data['name'], x=[], y=[])
            self.config['data_y'][data['name']] = []
        self._update()

    def _update(self):
        if len(self.config['data_x']) == 0:
            t = 1
        else:
            t = self.config['data_x'][-1] + 1
        self.config['data_x'].append(t)
        dpg.set_axis_limits(self.x_axis, self.config['data_x'][-1]-30, self.config['data_x'][-1])
        for i, (series_name, ser) in enumerate(self.config['series'].items()):
            self.config['data_y'][series_name].append(math.sin(time.monotonic()+i))
            dpg.set_value(ser, [self.config['data_x'], self.config['data_y'][series_name]])

    def render(self):
        self._update()
