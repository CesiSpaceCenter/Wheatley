import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data


class NumericBarWidget(BaseWidget):
    name = 'Numeric bar'

    config_definition = {
        'data point': config_types.DataPoint(),
        'custom label': config_types.Bool(default=False),
        'custom label value': config_types.Str(),
        'round': config_types.Int(default=2),
        'min': config_types.Int(default=0),
        'max': config_types.Int(default=100)
    }

    def __init__(self, *args):
        super(NumericBarWidget, self).__init__(*args)

        if self.config['data point'] == '':
            return

        data_point = Data.plugin.dictionary[self.config['data point']]  # get the datapoint config from the datastore

        # create the label, with a custom value if there is one
        if self.config['custom label']:
            label = self.config['custom label value']
        else:
            label = data_point.name

        self.label = dpg.add_text(
            default_value=label,
            parent=self.window
        )

        self.slider = dpg.add_slider_float(  # this slider is the one that will have the realtime datapoint value
            parent=self.window,
            width=-1,
            min_value=self.config['min'],
            max_value=self.config['max'],
            format=f'%.{self.config["round"]}f'
        )
        dpg.bind_item_font(self.slider, 'big')

        self.unit_text = dpg.add_text(
            default_value=Data.plugin.dictionary[self.config['data point']].unit,
            parent=self.window
        )

    def render(self):
        if self.config['data point'] == '':
            return

        data = Data.plugin.data[self.config['data point']]  # get the datapoint data from the datastore
        if len(data) == 0:  # don't proceed if there is no data yet
            return
        val = data[-1]  # take the last data point

        dpg.set_value(self.slider, round(val, self.config['round']))  # change the text

        window_w, window_h = dpg.get_item_rect_size(self.window)  # get the window size

        label_w, label_h = dpg.get_item_rect_size(self.label)  # get the label size
        dpg.set_item_pos(self.label, [window_w//2-label_w//2, 20])  # set the label at the center top of the of the window

        # do the same for the slider
        slider_w, slider_h = dpg.get_item_rect_size(self.slider)
        dpg.set_item_pos(self.slider, [window_w//2 - slider_w//2, window_h//2 - slider_h//2 + label_h])

        # and finally for the unit
        unit_w, unit_h = dpg.get_item_rect_size(self.unit_text)
        dpg.set_item_pos(self.unit_text, [window_w//2 - unit_w//2, window_h//2 - unit_h//2 + label_h + slider_h])

