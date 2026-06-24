import dearpygui.dearpygui as dpg
from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.fonts import Fonts


class DebugWidget(BaseWidget):
    name = 'Debug tool'

    def __init__(self, *args):
        super().__init__(*args)

        self.item_count = dpg.add_text(parent=self.window)
        self.widget_count = dpg.add_text(parent=self.window)
        self.global_timing = dpg.add_text(parent=self.window)

        self.widget_nodes = {}
        self.plugin_nodes = {}

        self.plugins_tree = dpg.add_tree_node(parent=self.window, label='Plugins')
        for plugin in self.widget_manager.plugin_manager.plugins:
            root = dpg.add_tree_node(label=type(plugin).__name__, parent=self.plugins_tree)
            self.plugin_nodes[plugin] = {
                'root': root,
                'timing': dpg.add_text(parent=root)
            }

        self.widgets_tree = dpg.add_tree_node(parent=self.window, label='Widgets')

        dpg.add_button(label='Open DPG debug tool', parent=self.window, callback=dpg.show_item_registry)

    def render(self):
        dpg.set_value(self.widget_count, f'Widgets count: {len(self.widget_manager.widgets)}')
        dpg.set_value(self.item_count, f'Items count: {len(dpg.get_all_items())}')
        t = self.widget_manager.plugin_manager.timings
        dpg.set_value(self.global_timing, f'Global render time: {round(sum(t)/len(t),3)}s')

        deleted_widgets = set(self.widget_nodes.keys()) - set(self.widget_manager.widgets)
        new_widgets = set(self.widget_manager.widgets) - set(self.widget_nodes.keys())
        for widget, node in list(self.widget_nodes.items()):
            if widget in deleted_widgets:
                print(widget)
                dpg.delete_item(node['root'])
                del self.widget_nodes[widget]
        for widget in new_widgets:
            root = dpg.add_tree_node(label=widget.name, parent=self.widgets_tree)
            self.widget_nodes[widget] = {
                'root': root,
                'timing': dpg.add_text(parent=root)
            }

        for plugin, nodes in self.plugin_nodes.items():
            t = plugin.timings
            dpg.set_value(nodes['timing'], f'render time = {round(sum(t)/len(t), 4)}s')

        for widget, nodes in self.widget_nodes.items():
            t = widget.timings
            if len(t) == 0:
                continue
            dpg.set_value(nodes['timing'], f'render time = {round(sum(t)/len(t), 4)}s')
