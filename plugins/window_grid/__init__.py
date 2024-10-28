import dearpygui.dearpygui as dpg
from plugins.base_plugin import BasePlugin


class WindowGrid(BasePlugin):
    def __init__(self):
        self.grid_size = 100
        self.enabled = True
        self.menubar_height = dpg.get_item_height('menubar')

        with dpg.menu(parent='menubar_settings', label='Window grid'):
            def toggle_grid(_, enabled):
                self.enabled = enabled
                self._draw_grid()
            dpg.add_checkbox(label='Enable grid', callback=toggle_grid, default_value=self.enabled)

            def update_grid(_, size):
                self.grid_size = size
                self._draw_grid()
            dpg.add_slider_int(label='Grid size', callback=update_grid, default_value=self.grid_size, min_value=10, max_value=200)

        with dpg.handler_registry():
            dpg.add_mouse_release_handler(callback=self._on_mouse_release)
            dpg.set_viewport_resize_callback(callback=self._draw_grid)

    def _on_mouse_release(self):
        if not self.enabled:
            return

        win = dpg.get_active_window()
        w = dpg.get_item_width(win)
        h = dpg.get_item_height(win)

        if w == 0 or h == 0:
            return

        win_config = dpg.get_item_configuration(win)
        if not win_config.get('no_resize', False) and not win_config.get('autosize', False):
            dpg.set_item_height(win, round(h / self.grid_size) * self.grid_size)
            dpg.set_item_width(win, round(w / self.grid_size) * self.grid_size)

        if not win_config.get('no_move', False):
            x, y = dpg.get_item_pos(win)
            y = y - self.menubar_height
            dpg.set_item_pos(win, [
                round(x / self.grid_size) * self.grid_size,
                round(y / self.grid_size) * self.grid_size + self.menubar_height
            ])

    def _draw_grid(self):
        if dpg.does_item_exist('viewport_grid'):
            dpg.delete_item('viewport_grid')

        if not self.enabled:
            return

        with dpg.viewport_drawlist(tag='viewport_grid', front=False):
            wp_width = dpg.get_viewport_width()
            wp_height = dpg.get_viewport_height()
            for x in range(self.grid_size, wp_width, self.grid_size):
                dpg.draw_line((x, 0), (x, wp_height), color=(255, 255, 255, 20))

            for y in range(self.grid_size + self.menubar_height, wp_height, self.grid_size):
                dpg.draw_line((0, y), (wp_width, y), color=(255, 255, 255, 20))

    def after_viewport(self):
        self._draw_grid()
