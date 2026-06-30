import dearpygui.dearpygui as dpg
from plugins.widgets.multiple_single_plots import MultipleSinglePlotsWidget
from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data


class AllDataPlotsWidget(MultipleSinglePlotsWidget):
    name = 'All data plots'

    config_definition = {
        **MultipleSinglePlotsWidget.config_definition,
        'series': config_types.Base()  # hide the config ui for series, it will be manually initialized
    }

    def __init__(self, *args):
        BaseWidget.__init__(self, *args)
        self.config['series'] = []

        for datapoint in Data.plugin.dictionary.values():
            self.config['series'].append(datapoint.name)

        MultipleSinglePlotsWidget.__init__(self, *args)
