from plugins.base_plugin import BasePlugin


class PluginManager:
    plugins = []

    def register(self, plugins: list[type[BasePlugin]]):
        """ Loads a list of plugins. __init__ will be called, and the plugin object will be stored in the class's plugin attribute """
        for plugin_class in plugins:
            plugin = plugin_class()
            plugin_class.plugin = plugin  # store the plugins object in a class attribute, so we can access the object by just importing the file
            self.plugins.append(plugin)

    def _call_for_all(self, method: str):
        """ calls a method for all the plugins """
        for plugin in self.plugins:
            if hasattr(plugin, method):  # only call the method if the method really exists
                getattr(plugin, method)()

    def after_viewport(self):
        """ Call every plugin's after_viewport method """
        self._call_for_all('after_viewport')

    def render(self):
        """ Call every plugin's render method """
        self._call_for_all('render')
