import dearpygui.dearpygui as dpg
from plugins.widgets.multiple_single_plots import MultipleSinglePlotsWidget
from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data


class AllDataPlotsWidget(MultipleSinglePlotsWidget):
    name = 'All data plots'

    config_definition = {
        **MultipleSinglePlotsWidget.config_definition,
        'x': config_types.DataPoint(),
        'series': config_types.Base()  # hide the config ui for series, it will be manually initialized
    }

    def __init__(self, *args):
        BaseWidget.__init__(self, *args)
        self.config['series'] = []

        if not self.config['x']:
            return

        for datapoint in Data.plugin.dictionary.values():
            if datapoint.name != self.config['x']:
                self.config['series'].append({
                    'x': self.config['x'],
                    'y': datapoint.name
                })

        MultipleSinglePlotsWidget.__init__(self, *args)
