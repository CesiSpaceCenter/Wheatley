import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget, Types


class TextWidget(BaseWidget):
    name = 'Text'

    config_definition = {
        'text': Types.Str(),
        'bullet': Types.Bool(default=False)
    }

    def __init__(self, *args):
        super(TextWidget, self).__init__(*args)
        self.text = dpg.add_text(
            default_value=self.config['text'],
            parent=self.window,
            bullet=self.config['bullet']
        )
