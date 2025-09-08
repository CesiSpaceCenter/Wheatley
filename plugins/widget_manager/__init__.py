import dearpygui.dearpygui as dpg

from plugins.base_plugin import BasePlugin
from plugins.base_widget import BaseWidget

from plugins.widgets.text import TextWidget
from plugins.widgets.plot import PlotWidget
from plugins.widgets.numeric import NumericWidget
from plugins.widgets.numeric_bar import NumericBarWidget
from plugins.widgets.status_table import StatusTableWidget
from plugins.widgets.multiple_single_plots import MultipleSinglePlotsWidget

# this class is mainly just to store widgets

class WidgetManager(BasePlugin):
    widget_types = [
        TextWidget,
        PlotWidget,
        NumericBarWidget,
        NumericWidget,
        StatusTableWidget,
        MultipleSinglePlotsWidget
    ]

    def __init__(self):
        super().__init__()
        self.widgets: list[BaseWidget] = []

        with dpg.menu(parent='menubar', label='Widget'):
            def add_widget_callback(_sender, _, widget_type: type[BaseWidget]):
                self.create_widget(widget_type)

            for widget in self.widget_types:  # add a menu item for each widget
                dpg.add_menu_item(label=widget.name, callback=add_widget_callback, user_data=widget)

    def create_widget(
        self,
        widget_type: type[BaseWidget],
        window_config: dict[str, any] | None = None,
        widget_config: dict[str, any] | None = None,
        window_tag: str | int | None = None
    ):
        """ creates a new widget and adds it to the registry """
        widget = widget_type(window_config, widget_config, window_tag)
        self.widgets.append(widget)
        self.logger.info(f'Creating widget {widget}')
        widget.ready = True

    def reset_widget(
        self,
        widget: BaseWidget,
        window_config: dict[str, any] | None = None,
        widget_config: dict[str, any] | None = None
    ):
        """ re-initialize a widget with new widget_config and window_config """
        window_config = window_config if window_config is not None else widget.window_config
        widget_config = widget_config if widget_config is not None else widget.config
        window_tag = widget.window
        widget_type = type(widget)
        index = self.widgets.index(widget)
        self.widgets[index] = widget_type(window_config, widget_config, window_tag)
        self.widgets[index].ready = True
        self.logger.info(f'Reset widget {widget}, new: {self.widgets[index]}')
        return self.widgets[index]

    def delete_widget(self, widget: BaseWidget):
        """ closes a widget window and remove it from the registry """
        self.logger.info(f'Deleting widget {widget}')
        if dpg.does_item_exist(widget.window):
            dpg.delete_item(widget.window)
        self.widgets.remove(widget)
