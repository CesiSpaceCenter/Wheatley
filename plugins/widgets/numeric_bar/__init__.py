import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.data_store import DataStore
from plugins.fonts import Fonts


class NumericBarWidget(BaseWidget):
    default_config = {
        'data_point': 'accx',
        'custom_label': False,
        'custom_label_value': '',
        'round': 2,
        'min': 0,
        'max': 100
    }

    default_window_config = {
    }

    def __init__(self, *args):
        super(NumericBarWidget, self).__init__(*args)

        data_point = DataStore.plugin.dictionary[self.config['data_point']]

        if self.config['custom_label']:
            label = self.config['custom_label_value']
        else:
            label = data_point['name']

        self.label = dpg.add_text(
            default_value=label,
            parent=self.window
        )

        self.slider = dpg.add_slider_float(
            parent=self.window,
            width=-1,
            min_value=self.config['min'],
            max_value=self.config['max']
        )
        dpg.bind_item_font(self.slider, 'big')

    def render(self):
        data = DataStore.plugin.data[self.config['data_point']]
        if len(data) == 0:
            return
        val = data[-1]

        if self.config['round'] <= 0:
            val = int(val)
        else:
            #val = '{:.{}f}'.format(val, self.config['round'])
            val = round(val, self.config['round'])
        dpg.set_value(self.slider, val)

        ww, wh = dpg.get_item_rect_size(self.window)

        label_w, label_h = dpg.get_item_rect_size(self.label)
        dpg.set_item_pos(self.label, [ww//2-label_w//2, 20])

        slider_w, slider_h = dpg.get_item_rect_size(self.slider)
        dpg.set_item_pos(self.slider, [ww//2 - slider_w//2, wh//2 - slider_h//2 + label_h])

