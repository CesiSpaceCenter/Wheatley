import dearpygui.dearpygui as dpg

from plugins.base_plugin import BasePlugin
from utils import get_widget
from plugins.base_widget import BaseWidget
from plugins.config_ui import ConfigUI

class WidgetConfig(BasePlugin):
    def __init__(self):
        self.window = dpg.add_window(label='Widget config', width=300, height=600)
        self.active_widget: BaseWidget = None
        # the next 2 dict will store the temporary new config. they are updated in real-time with the inputs
        self.new_widget_config: dict = None
        self.new_window_config: dict = None

    def render_config_window(self):
        """ Re-create inputs depending on the selected widget's config """
        dpg.delete_item(self.window, children_only=True)  # remove all existing inputs

        def callback(window_config, widget_config):  # callback for when the window or widget config is updated
            new_widget = type(self.active_widget)(  # create a new widget
                window_config if window_config is not None else self.active_widget.window_config,
                widget_config if widget_config is not None else self.active_widget.config,
                self.active_widget.window
            )
            self.active_widget = new_widget
            new_widget.ready = True  # set widget ready only after __init__ is done

        dpg.add_separator(parent=self.window, label='Window config')
        ConfigUI(self.window, self.active_widget.window_config_definition, self.active_widget.window_config, lambda conf: callback(conf, None))

        dpg.add_separator(parent=self.window, label='Widget config')
        ConfigUI(self.window, self.active_widget.config_definition, self.active_widget.config, lambda conf: callback(None, conf))

    def render(self):
        # udate the active widget
        active_window = dpg.get_active_window()
        if active_window == self.window:  # abort if the selected window is the widget config window
            return

        widget = get_widget(active_window)
        if widget:  # selected window is a widget
            if self.active_widget == widget:  # abort if the selected widget has not changed
                return
            # different widget selected
            self.new_widget_config = {}
            self.new_window_config = {}
            self.active_widget = widget
            self.render_config_window()

        if not widget and self.active_widget is not None:  # selected window is not a widget
            self.active_widget = None
            dpg.delete_item(self.window, children_only=True)
