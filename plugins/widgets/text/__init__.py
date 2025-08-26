import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types


class TextWidget(BaseWidget):
    name = 'Text'

    config_definition = {
        'text': config_types.Str(),
        'bullet': config_types.Bool(default=False)
    }

    def __init__(self, *args):
        super(TextWidget, self).__init__(*args)
        self.text = dpg.add_text(
            default_value=self.config['text'],
            parent=self.window,
            bullet=self.config['bullet']
        )
