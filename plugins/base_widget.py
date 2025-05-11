import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin
from uuid import uuid4


class BaseWidget(BasePlugin):
    default_config: dict  # widget default configuration
    config: dict  # widget current configuration
    default_window_config: dict  # widget's window default configuration
    window_config = {  # widget's window current configuration (dpg.window keyword arguments
        'label': 'Widget',
        'no_scrollbar': False,
        'no_scroll_with_mouse': False
    }
    window: int  # widget's window tag

    # safeguard, because dpg is multithreaded, and the main loop might run before __init__ is done
    # the render() function will not run unless this is true
    ready = False

    def __init__(self, window_config=None, widget_config=None, window_tag=None):
        if window_config is None:  # if no custom window config has been set for this widget instance
            # combine the base window config with the widget's default window config
            self.window_config = {**self.window_config, **self.default_window_config}
        else:  # a custom window config is present for this widget instance
            # combine the base window config with this widget's instance window config
            self.window_config = {**self.window_config, **window_config}

        # in case we want to create a widget with an existing window
        # don't recreate the window, only reconfigure it, and delete all of its childrens
        if window_tag is not None and dpg.does_item_exist(window_tag):
            self.window = window_tag
            # https://github.com/hoffstadt/DearPyGui/issues/1625
            # don't reconfigure label if it hasn't changed, otherwise it will break the docking
            window_config = self.window_config.copy()
            if dpg.get_item_label(self.window) == window_config['label']:
                del window_config['label']
            dpg.configure_item(self.window, **window_config, user_data=self)  # user_data is the widget instance object
            dpg.delete_item(self.window, children_only=True)
        else:  # new window
            # generate a random unique (enough) window tag
            # we need to use an integer for the window tag, because dpg's init file only works this way
            window_tag = int(str(uuid4().int)[:8])
            self.window = dpg.add_window(**self.window_config, user_data=self, tag=window_tag)  # user_data is the widget instance object

        if widget_config is None:  # no custom config for this widget instance
            self.config = self.default_config  # use the widget default config
        else:
            self.config = widget_config

    def render(self):
        """ Widget main loop, code to be run at every render loop """
        pass

    def after_viewport(self):
        """ Code to be run just after the viewport has been setup, but before the main loop """
        pass
