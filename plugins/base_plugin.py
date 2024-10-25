from typing import Self


class BasePlugin:
    plugin: Self

    def render(self):
        pass

    def after_viewport(self):
        pass
