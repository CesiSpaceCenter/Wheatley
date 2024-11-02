import dearpygui.dearpygui as dpg


should_close = False
should_restart = False


def start_app():
    global should_restart
    while not should_close or (should_close and should_restart):
        if should_restart:
            should_restart = False
        run()


def run():
    global should_close
    from plugins import (
        menu_bar,
        fonts,
        app,
        loading,
        widget_config,
        data_store
    )
    import plugins

    dpg.create_context()

    plugin_manager = plugins.PluginManager()
    plugin_manager.register([
        menu_bar.MenuBar,
        fonts.Fonts,
        loading.Loading,
        data_store.DataStore,
        widget_config.WidgetConfig,
        app.App,
    ])

    dpg.create_viewport(title='Wheatley', small_icon='icon.png', large_icon='icon.png')
    dpg.setup_dearpygui()
    dpg.show_viewport()

    plugin_manager.after_viewport()

    while dpg.is_dearpygui_running():
        plugin_manager.render()
        dpg.render_dearpygui_frame()
        if should_restart:
            dpg.stop_dearpygui()

    should_close = True
    dpg.destroy_context()
