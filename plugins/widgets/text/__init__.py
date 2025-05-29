import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget


class TextWidget(BaseWidget):
    name = 'Text'

    config_definition = {
        'text': (str, ''),
        'bullet': (bool, False)
    }

    def __init__(self, *args):
        super(TextWidget, self).__init__(*args)
        self.text = dpg.add_text(
            default_value=self.config['text'],
            parent=self.window,
            bullet=self.config['bullet']
        )
