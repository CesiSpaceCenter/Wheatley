import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.data_store import DataStore
from plugins.fonts import Fonts


class NumericWidget(BaseWidget):
    default_config = {
        'data_point': 'accx',
        'custom_label': False,
        'custom_label_value': '',
        'round': 2
    }

    default_window_config = {
    }

    def __init__(self, window_config=None, widget_config=None):
        super(NumericWidget, self).__init__(window_config, widget_config)

        data_point = DataStore.plugin.dictionary[self.config['data_point']]

        if self.config['custom_label']:
            label = self.config['custom_label_value']
        else:
            label = data_point['name']

        self.label = dpg.add_text(
            default_value=label,
            parent=self.window
        )

        self.text = dpg.add_text(
            parent=self.window
        )
        dpg.bind_item_font(self.text, 'big')

    def render(self):
        val = DataStore.plugin.data[self.config['data_point']][-1]
        if self.config['round'] <= 0:
            val = int(val)
        else:
            val = '{:.{}f}'.format(val, self.config['round'])
        dpg.configure_item(self.text, default_value=val)

        ww, wh = dpg.get_item_rect_size(self.window)

        label_w, label_h = dpg.get_item_rect_size(self.label)
        dpg.set_item_pos(self.label, [ww//2-label_w//2, 20])

        text_w, text_h = dpg.get_item_rect_size(self.text)
        dpg.set_item_pos(self.text, [ww//2 - text_w//2, wh//2 - text_h//2 + label_h])

