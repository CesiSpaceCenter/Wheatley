from typing import Self

# only used for typing


class BasePlugin:
    plugin: Self  # access to the plugin singleton object

    def render(self):
        """ Plugin main loop, code to be run at every render loop """
        pass

    def after_viewport(self):
        """ Code to be run just after the viewport has been setup, but before the main loop """
        pass
