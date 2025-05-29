import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget
from plugins.data_store import DataStore
from plugins.widget_config import DataPoint, DataPointArray


class PlotWidget(BaseWidget):
    name = 'Plot'

    config_definition = {
        'data_point_x': (DataPoint, 't'),
        'data_point_y': (DataPointArray, [])
    }

    def __init__(self, *args):
        super(PlotWidget, self).__init__(*args)

        self.plot = dpg.add_plot(parent=self.window, width=-1, height=-1)
        dpg.add_plot_legend(parent=self.plot)

        print('data_point_y for plot', self.config['data_point_y'])
        # horizontal axis
        self.x_axis = dpg.add_plot_axis(axis=dpg.mvXAxis, parent=self.plot, label=self.config['data_point_x'])

        self.series = {}  # dict that will store every dpg's Series
        self.y_axis = {}  # dict that will store every dpg's YAxis

        for data_point_id in self.config['data_point_y']:
            data_point = DataStore.plugin.dictionary[data_point_id]  # get the datapoint config from the datastore

            # every y axis represents a unit
            if data_point['unit'] not in self.y_axis:
                # dpg limits to 3 y axis, so choose between mvYAxis, mvYAxis2, mvYAxis3
                if len(self.y_axis) > 2:
                    raise Exception('Reached limit of 3 y axis')
                axis = [dpg.mvYAxis, dpg.mvYAxis2, dpg.mvYAxis3][len(self.y_axis)]
                # create the y_axis
                self.y_axis[data_point['unit']] = dpg.add_plot_axis(axis=axis, parent=self.plot, label=data_point['unit'])

            # create the series
            self.series[data_point_id] = dpg.add_line_series(
                parent=self.y_axis[data_point['unit']],
                label=data_point['name'],
                x=[],
                y=[]
            )

    def render(self):
        # get the datapoit's data from the datastore
        data = DataStore.plugin.data
        data_x = data[self.config['data_point_x']]
        if len(data_x) == 0:  # ignore if there is no data yet
            return

        # update the axis limits to fit with new the data
        dpg.set_axis_limits(self.x_axis, data_x[-1] - 30, data_x[-1])
        for series_name, ser in self.series.items():
            if len(data[series_name]) == 0:  # ignore if there is no data yet
                continue
            dpg.set_value(ser, [data_x, data[series_name]])  # update the series with the new x and y data
