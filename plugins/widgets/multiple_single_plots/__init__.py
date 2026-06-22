import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data


class MultipleSinglePlotsWidget(BaseWidget):
    name = 'Multiple single plots'

    config_definition = {
        'plot height': config_types.Int(default=150),
        'auto plot height': config_types.Bool(default=True),
        'link x axes': config_types.Bool(default=False),
        'series': config_types.List(config_types.Group({
            'x': config_types.DataPoint(),
            'y': config_types.DataPoint()
        }))
    }

    def __init__(self, *args):
        if type(self) == MultipleSinglePlotsWidget:  # don't init parent if MultipleSinglePlotsWidget is inherited (all_data_plots widget)
            super(MultipleSinglePlotsWidget, self).__init__(*args)

        self.plots = []

        with dpg.theme() as container_theme:
            with dpg.theme_component(dpg.mvWindowAppItem):
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0)
            dpg.bind_item_theme(self.window, container_theme)

        if self.config['auto plot height']:
            subplot_height = -1
        else:
            subplot_height = len(self.config['series']) * self.config['plot height']

        subplot = dpg.add_subplots(len(self.config['series']), 1, parent=self.window, width=-1, height=subplot_height, link_all_x=self.config['link x axes'])

        for i, ser in enumerate(self.config['series']):
            datapoint_x = Data.plugin.dictionary[ser['x']]
            datapoint_y = Data.plugin.dictionary[ser['y']]

            plot = dpg.add_plot(parent=subplot, width=-1)

            x_axis = dpg.add_plot_axis(axis=dpg.mvXAxis, parent=plot, label=datapoint_x.name + (f' ({datapoint_x.unit})' if datapoint_x.unit else ''))
            y_axis = dpg.add_plot_axis(axis=dpg.mvYAxis, parent=plot, label=datapoint_y.name + (f' ({datapoint_y.unit})' if datapoint_y.unit else ''))

            series = dpg.add_line_series(
                parent=y_axis,
                x=[],
                y=[]
            )

            self.plots.append({
                'plot': plot,
                'x_axis': x_axis,
                'y_axis': y_axis,
                'x': ser['x'],
                'y': ser['y'],
                'series': series
            })

    def render(self):
        if not Data.plugin.has_changed and not self.reload:
            return

        if not self.config['series']:  # ignore if no datapoint has been configured
            return

        Data.plugin.has_changed = False

        # get the datapoint's data from the datastore
        data = Data.plugin.data

        # update the axis limits to fit with new the data
        for plot in self.plots:
            if len(data[plot['x']]) == 0 or len(data[plot['x']]) == 0:  # ignore if there is no data yet
                continue

            data_x = data[plot['x']]
            data_y = data[plot['y']]

            dpg.set_value(plot['series'], [data_x, data_y])  # update the series with the new x and y data

            dpg.set_axis_limits(plot['x_axis'], data_x[0], data_x[-1])
            dpg.set_axis_limits(plot['y_axis'], min(data_y)-1, max(data_y)+1)
