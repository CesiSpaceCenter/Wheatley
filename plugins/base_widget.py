import dearpygui.dearpygui as dpg
from uuid import uuid4
from typing import Any
import copy

from plugins.base_plugin import BasePlugin

class Types:
    class Base:
        _default: Any
        base_default: Any = None
        config: Any

        def default(self):
            # returns either a new copy of self._default (default value of the config item represented by this type),
            # or a new copy of self.base_default (default value of this type)
            return copy.deepcopy(self._default if self._default is not None else self.base_default)

        def __init__(self, config=None, default=None):
            self._default = default
            self.config = config if config is not None else {}

        def parse(self, val: Any):
            pass

    class List(Base):
        base_default = []
        def parse(self, val: Any):
            return list(val)

    class DataPoint(Base):
        base_default = ''

        def parse(self, val: Any):
            return str(val)

    class Group(Base):
        base_default = None

        def __init__(self, *args, **kwargs):
            super(Types.Group, self).__init__(*args, **kwargs)
            if self.default() is None:
                self._default = {}
                for k, v in self.config.items():
                    self._default[k] = v.default()

        def parse(self, val: Any):
            return dict(val)

    class Str(Base):
        base_default = ''

        def parse(self, val: Any):
            return str(val)

    class Int(Base):
        base_default = 0

        def parse(self, val: Any):
            return int(val)

    class Bool(Base):
        base_default = False

        def parse(self, val: Any):
            return bool(val)

    class Text(Base):
        pass


class BaseWidget(BasePlugin):
    name: str  # user-friendly name

    config_definition: dict[str, Types.Base] = {}  # widget default configuration & configuration types
    config: dict[str, any] = {}  # widget current configuration

    window_config_definition: dict[str, Types.Base] = {}  # widget's window default configuration & configuration types
    window_config: dict[str, any] = {}  # widget's window current configuration (dpg.window keyword arguments)

    window: int  # widget's window tag

    # safeguard, because dpg is multithreaded, and the main loop might run before __init__ is done
    # the render() function will not run unless this is true
    ready = False

    def __init__(self, window_config : dict[str, any] = None, widget_config : dict[str, any] = None, window_tag : int = None):
        # add some window config for all widget
        self.window_config_definition['label'] = Types.Str()
        self.window_config_definition['no_scrollbar'] = Types.Bool(default=False)
        self.window_config_definition['no_scroll_with_mouse'] = Types.Bool(default=False)

        # reset config & window config
        self.config = {}
        self.window_config = {}

        # create the final window config & widget config from the user-defined config & the default config

        for k, v in self.window_config_definition.items():
            if window_config is not None and k in window_config:  # this config key has been defined in the config
                self.window_config[k] = window_config[k]
            else:
                self.window_config[k] = v.default()  # use the default value for this config key

        for k, v in self.config_definition.items():
            if widget_config is not None and k in widget_config:  # this config key has been defined in the config
                self.config[k] = widget_config[k]
            else:
                self.config[k] = v.default()  # use the default value for this config key

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

    def render(self):
        """ Widget main loop, code to be run at every render loop """
        pass

    def after_viewport(self):
        """ Code to be run just after the viewport has been setup, but before the main loop """
        pass
