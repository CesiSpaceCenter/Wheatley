import dearpygui.dearpygui as dpg

# the app will continuously restart while this is True
# false by default when the app is running
# to restart the app, set this to true and close dpg
should_run = True


def start_app():  # entrypoint
    global should_run
    while should_run:
        should_run = False  # will not run when closed, unless changed to true
        run()


def run():
    dpg.create_context()

    # import every needed plugins
    from plugins import (
        menu_bar,
        fonts,
        app,
        loading,
        widget_config,
        data_store
    )
    # initialize plugin manager
    import plugins
    plugin_manager = plugins.PluginManager()
    # register all needed plugins
    plugin_manager.register([
        menu_bar.MenuBar,
        fonts.Fonts,
        loading.Loading,
        data_store.DataStore,
        widget_config.WidgetConfig,
        app.App,
    ])

    # setup the main viewport & dpg
    dpg.create_viewport(title='Wheatley', small_icon='icon.png', large_icon='icon.png')
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # run every plugin's code that need to be run after viewport setup, before main loop
    plugin_manager.after_viewport()

    while dpg.is_dearpygui_running():  # main render loop
        plugin_manager.render()  # run every plugin's main loop code
        dpg.render_dearpygui_frame()  # render dpg

    dpg.destroy_context()
