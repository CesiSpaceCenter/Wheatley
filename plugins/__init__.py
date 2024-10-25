from plugins.base_plugin import BasePlugin


class PluginManager:
    plugins = []

    def register(self, plugins: list[type[BasePlugin]]):
        for plugin_class in plugins:
            plugin = plugin_class()
            plugin_class.plugin = plugin
            self.plugins.append(plugin)

    def _call_for_all(self, method: str):
        for plugin in self.plugins:
            if hasattr(plugin, method):
                getattr(plugin, method)()

    def after_viewport(self):
        self._call_for_all('after_viewport')

    def render(self):
        self._call_for_all('render')
