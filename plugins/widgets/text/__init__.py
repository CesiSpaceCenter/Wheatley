import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget


class TextWidget(BaseWidget):
    config = {
        'text': '',
        'bullet': False
    }

    default_window_config = {
        'autosize': True
    }

    def __init__(self, window_config=None, widget_config=None):
        super(TextWidget, self).__init__(window_config, widget_config)
        self.text = dpg.add_text(
            default_value=self.config['text'],
            parent=self.window,
            bullet=self.config['bullet']
        )
