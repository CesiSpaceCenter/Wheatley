from threading import Thread
import logging
from plugins.config_ui import config_types


class DataSource:
    config_definition: dict[str, config_types.Base] = {}
    config: dict[str, any] = {}

    def __init__(self, data_changed_callback: callable, metadata_changed_callback: callable):
        self.logger = logging.getLogger(type(self).__name__)
        self.data_changed_callback = data_changed_callback
        self.metadata_changed_callback = metadata_changed_callback
        self.thread = Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        pass

    def config_changed(self, config: dict[str, any]):
        pass
