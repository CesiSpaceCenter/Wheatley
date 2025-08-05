import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.data_store import DataStore
from plugins.widget_config import DataPoint


class NumericWidget(BaseWidget):
    name = 'Numeric'

    config_definition = {
        'data_point': (DataPoint, 'accx'),
        'custom_label': (bool, False),
        'custom_label_value': (str, ''),
        'round': (int, 2)
    }

    def __init__(self, *args):
        super(NumericWidget, self).__init__(*args)

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

        self.value_text = dpg.add_text(  # this text is the one that will have the realtime datapoint value
            parent=self.window
        )
        dpg.bind_item_font(self.value_text, 'big')

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
            # don't use round(), because we want to keep trailing zeros (we want 1.100, round() will give us 1.1)
            val = '{:.{}f}'.format(val, self.config['round'])
        dpg.configure_item(self.value_text, default_value=val)  # change the text

        window_w, window_h = dpg.get_item_rect_size(self.window)  # get the window size

        label_w, label_h = dpg.get_item_rect_size(self.label)  # get the label size
        dpg.set_item_pos(self.label, [window_w//2-label_w//2, 20])  # set the label at the center top of the window

        # do the same for the value text
        value_w, value_h = dpg.get_item_rect_size(self.value_text)
        dpg.set_item_pos(self.value_text, [window_w // 2 - value_w // 2, window_h // 2 - value_h // 2 + label_h])

        # and finally for the unit
        unit_w, unit_h = dpg.get_item_rect_size(self.unit_text)
        dpg.set_item_pos(self.unit_text, [window_w//2 - unit_w//2, window_h//2 - unit_h//2 + label_h + value_h])

