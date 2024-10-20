import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget


class TextWidget(BaseWidget):
    config = {
        'text': '',
        'bullet': False
    }

    window_config = {
        'autosize': True
    }

    def __init__(self, window_config=None, widget_config=None):
        super(TextWidget, self).__init__(window_config, widget_config)
        self.text = dpg.add_text(
            default_value=self.config['text'],
            parent=self.window,
            bullet=self.config['bullet']
        )

    def config_updated(self, config_name: str, config_value: any):
        match config_name:
            case 'text':
                dpg.configure_item(self.text, default_value=config_value)
            case 'bullet':
                dpg.configure_item(self.text, bullet=config_value)
