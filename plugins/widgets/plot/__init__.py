import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget
from plugins.data_store import DataStore


class PlotWidget(BaseWidget):
    default_config = {
        'data_points': ['accx'],
        'data_point_x': 't'
    }

    default_window_config = {
    }

    def __init__(self, *args):
        super(PlotWidget, self).__init__(*args)

        self.plot = dpg.add_plot(parent=self.window, width=-1, height=-1)
        dpg.add_plot_legend(parent=self.plot)

        self.x_axis = dpg.add_plot_axis(axis=dpg.mvXAxis, parent=self.plot, label=self.config['data_point_x'])

        self.series = {}
        self.y_axis = {}

        for data_point_id in self.config['data_points']:
            data_point = DataStore.plugin.dictionary[data_point_id]

            if data_point['unit'] not in self.y_axis:
                axis = [dpg.mvYAxis, dpg.mvYAxis2, dpg.mvYAxis3][len(self.y_axis)]
                self.y_axis[data_point['unit']] = dpg.add_plot_axis(axis=axis, parent=self.plot, label=data_point['unit'])

            self.series[data_point_id] = dpg.add_line_series(
                parent=self.y_axis[data_point['unit']],
                label=data_point['name'],
                x=[],
                y=[]
            )

    def _update(self):
        data = DataStore.plugin.data
        data_x = data[self.config['data_point_x']]
        if len(data_x) == 0:
            return

        dpg.set_axis_limits(self.x_axis, data_x[-1]-30, data_x[-1])
        for series_name, ser in self.series.items():
            if len(data[series_name]) == 0:
                continue
            dpg.set_value(ser, [data_x, data[series_name]])

    def render(self):
        self._update()
