import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.data_store import DataStore
from plugins.widget_config import DataPoint


class NumericBarWidget(BaseWidget):
    name = 'Numeric bar'

    config_definition = {
        'data_point': (DataPoint, 'accx'),
        'custom_label': (bool, False),
        'custom_label_value': (str, ''),
        'round': (int, 2),
        'min': (int, 0),
        'max': (int, 100)
    }

    def __init__(self, *args):
        super(NumericBarWidget, self).__init__(*args)

        data_point = DataStore.plugin.dictionary[self.config['data_point']]  # get the datapoint config from the datastore

        # create the label, with a custom value if there is one
        if self.config['custom_label']:
            label = self.config['custom_label_value']
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
            max_value=self.config['max']
        )
        dpg.bind_item_font(self.slider, 'big')

        self.unit_text = dpg.add_text(
            default_value=DataStore.plugin.dictionary[self.config['data_point']].unit,
            parent=self.window
        )

    def render(self):
        data = DataStore.plugin.data[self.config['data_point']]  # get the datapoint data from the datastore
        if len(data) == 0:  # don't proceed if there is no data yet
            return
        val = data[-1]  # take the last data point

        if self.config['round'] <= 0:  # no decimals
            val = int(val)
        else:
            val = round(val, self.config['round'])
        dpg.set_value(self.slider, val)  # change the text

        window_w, window_h = dpg.get_item_rect_size(self.window)  # get the window size

        label_w, label_h = dpg.get_item_rect_size(self.label)  # get the label size
        dpg.set_item_pos(self.label, [window_w//2-label_w//2, 20])  # set the label at the center top of the of the window

        # do the same for the slider
        slider_w, slider_h = dpg.get_item_rect_size(self.slider)
        dpg.set_item_pos(self.slider, [window_w//2 - slider_w//2, window_h//2 - slider_h//2 + label_h])

        # and finally for the unit
        unit_w, unit_h = dpg.get_item_rect_size(self.unit_text)
        dpg.set_item_pos(self.unit_text, [window_w//2 - unit_w//2, window_h//2 - unit_h//2 + label_h + slider_h])

