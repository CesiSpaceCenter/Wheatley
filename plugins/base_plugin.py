from typing import Self, TYPE_CHECKING
import logging
import time
if TYPE_CHECKING:
    from plugins import PluginManager

# only used for typing & logging initialization

class ThrottlingFilter(logging.Filter):
    def __init__(self, name='', rate_limit_seconds=5):
        super().__init__(name)
        self.rate_limit_seconds = rate_limit_seconds
        self.last_seen = {}

    def filter(self, record):
        msg = str(record.msg)
        now = time.time()

        if msg in self.last_seen:
            last_logged = self.last_seen[msg]
            # do not print the message if it was displayed less than rate_limit_seconds ago
            if now - last_logged < self.rate_limit_seconds:
                return False

        # if it has been more that rate_limit_seconds, update the last_seen and display the message
        self.last_seen[msg] = now
        return True

class BasePlugin:
    plugin: Self  # access to the plugin singleton object
    plugin_manager: PluginManager

    def __init__(self, manager: PluginManager):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.addFilter(ThrottlingFilter(rate_limit_seconds=3))
        self.plugin_manager = manager
        self.timings: list[float] = []

    def render(self):
        """ Plugin main loop, code to be run at every render loop """
        pass

    def after_viewport(self):
        """ Code to be run just after the viewport has been setup, but before the main loop """
        pass

    def stop(self):
        """ Code to be run when the app is to be closed """
        pass
