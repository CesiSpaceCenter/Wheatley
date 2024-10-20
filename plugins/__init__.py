class PluginManager:
    plugins = []

    def register(self, plugins: list):
        for plugin in plugins:
            self.plugins.append(plugin())

    def _call_for_all(self, method: str):
        for plugin in self.plugins:
            if hasattr(plugin, method):
                getattr(plugin, method)()

    def after_viewport(self):
        self._call_for_all('after_viewport')

    def render(self):
        self._call_for_all('render')
