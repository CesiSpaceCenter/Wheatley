import dearpygui.dearpygui as dpg

from plugins import app, window_grid, widget_config, loading
import plugins

dpg.create_context()

with dpg.viewport_menu_bar(tag='menubar'):
    dpg.add_menu(tag='menubar_settings', label='Settings')

plugin_manager = plugins.PluginManager()
plugin_manager.register([
    app.App,
    widget_config.WidgetConfig,
    window_grid.WindowGrid,
    loading.Loading
])

dpg.create_viewport(title='RCHC')
dpg.setup_dearpygui()
dpg.show_viewport()

plugin_manager.after_viewport()

while dpg.is_dearpygui_running():
    plugin_manager.render()
    dpg.render_dearpygui_frame()
dpg.destroy_context()
