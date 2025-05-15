import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget


class TextWidget(BaseWidget):
    name = 'Text'

    default_config = {
        'text': '',
        'bullet': False
    }

    default_window_config = {
    }

    def __init__(self, *args):
        super(TextWidget, self).__init__(*args)
        self.text = dpg.add_text(
            default_value=self.config['text'],
            parent=self.window,
            bullet=self.config['bullet']
        )
