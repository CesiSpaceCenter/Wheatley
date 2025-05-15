import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.data_store import DataStore
from plugins.widget_config import DataPoint


class NumericWidget(BaseWidget):
    name = 'Numeric'

    default_config = {
        'data_point': DataPoint('accx'),
        'custom_label': False,
        'custom_label_value': '',
        'round': 2,
        'add': 0
    }

    default_window_config = {
    }

    def __init__(self, *args):
        super(NumericWidget, self).__init__(*args)

        data_point = DataStore.plugin.dictionary[self.config['data_point']]  # get the datapoint config from the datastore

        # create the label, with a custom value if there is one
        if self.config['custom_label']:
            label = self.config['custom_label_value']
        else:
            label = data_point['name']

        self.label = dpg.add_text(
            default_value=label,
            parent=self.window
        )

        self.text = dpg.add_text(  # this text is the one that will have the realtime datapoint value
            parent=self.window
        )
        dpg.bind_item_font(self.text, 'big')

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
        dpg.configure_item(self.text, default_value=val)  # change the text

        ww, wh = dpg.get_item_rect_size(self.window)  # get the window size

        label_w, label_h = dpg.get_item_rect_size(self.label)  # get the label size
        dpg.set_item_pos(self.label, [ww//2-label_w//2, 20])  # set the label at the center top of the of the window

        # do the same for the text
        text_w, text_h = dpg.get_item_rect_size(self.text)
        dpg.set_item_pos(self.text, [ww//2 - text_w//2, wh//2 - text_h//2 + label_h])

