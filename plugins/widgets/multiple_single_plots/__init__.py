import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget, Types
from plugins.data import Data


class MultipleSinglePlotsWidget(BaseWidget):
    name = 'Multiple single plots'

    config_definition = {
        'plot height': Types.Int(default=150),
        'auto plot height': Types.Bool(default=True),
        'link x axes': Types.Bool(default=False),
        'series': Types.List(Types.Group({
            'x': Types.DataPoint(),
            'y': Types.DataPoint()
        }))
    }

    reload = False

    def __init__(self, *args):
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

        self.reload = True

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
        for plot in self.plots:
            if len(data[plot['x']]) == 0 or len(data[plot['x']]) == 0:  # ignore if there is no data yet
                continue

            data_x = data[plot['x']]
            data_y = data[plot['y']]

            dpg.set_value(plot['series'], [data_x, data_y])  # update the series with the new x and y data
