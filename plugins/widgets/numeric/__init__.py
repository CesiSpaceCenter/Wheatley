import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget, WidgetConfigItem
from plugins.data_store import DataStore
from plugins.widget_config import DataPoint


class NumericWidget(BaseWidget):
    name = 'Numeric'

    config_definition = {
        'data_point': WidgetConfigItem(DataPoint, 'accx'),
        'custom_label': WidgetConfigItem(bool, False),
        'custom_label_value': WidgetConfigItem(str, ''),
        'round': WidgetConfigItem(int, 2),
        'show detail': WidgetConfigItem(bool, True)
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

        self.avg_text = dpg.add_text(
            parent=self.window
        )
        self.min_text = dpg.add_text(
            parent=self.window
        )
        self.max_text = dpg.add_text(
            parent=self.window
        )

    def round(self, value: int | float) -> str:
        if self.config['round'] <= 0:  # no decimals
            return str(int(value))
        else:
            # don't use round(), because we want to keep trailing zeros (we want 1.100, round() will give us 1.1)
            return '{:.{}f}'.format(value, self.config['round'])

    def render(self):
        data = DataStore.plugin.data[self.config['data_point']]  # get the datapoint data from the datastore
        if len(data) == 0:  # don't proceed if there is no data yet
            return

        dpg.configure_item(self.value_text, default_value=self.round(data[-1]))  # set the text to the last data value
        if self.config['show detail']:
            dpg.configure_item(self.avg_text, default_value='avg '+self.round(sum(data)/len(data)))  # set the text to the average data value
            dpg.configure_item(self.min_text, default_value='min '+self.round(min(data)))  # set the text to the minimum data value
            dpg.configure_item(self.max_text, default_value='max '+self.round(max(data)))  # set the text to the maximum data value

        window_w, window_h = dpg.get_item_rect_size(self.window)  # get the window size

        label_w, label_h = dpg.get_item_rect_size(self.label)  # get the label size
        dpg.set_item_pos(self.label, [window_w//2-label_w//2, 20])  # set the label at the center top of the window

        # TODO: find a way to simplify or automate the text centering

        # do the same for the value text
        value_w, value_h = dpg.get_item_rect_size(self.value_text)
        dpg.set_item_pos(self.value_text, [window_w//2 - value_w//2, window_h//2 - value_h//2])

        # for the unit
        unit_w, unit_h = dpg.get_item_rect_size(self.unit_text)
        dpg.set_item_pos(self.unit_text, [window_w//2 - value_w//2 + value_w, window_h//2])

        if self.config['show detail']:
            # for the avg
            avg_w, avg_h = dpg.get_item_rect_size(self.avg_text)
            dpg.set_item_pos(self.avg_text, [window_w//2 - avg_w//2, window_h//2 - avg_h//2 + value_h + 2*unit_h])

            # for the min
            min_w, min_h = dpg.get_item_rect_size(self.min_text)
            dpg.set_item_pos(self.min_text, [window_w//2 - min_w//2, window_h//2 - min_h//2 + value_h + 2*unit_h + avg_h])

            # for the max
            max_w, max_h = dpg.get_item_rect_size(self.max_text)
            dpg.set_item_pos(self.max_text, [window_w//2 - max_w//2, window_h//2 - max_h//2 + value_h + 2*unit_h + avg_h + min_h])

