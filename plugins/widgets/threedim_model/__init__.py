
import time
from typing import Optional
import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data
import logging
logging.getLogger('moderngl_window').setLevel(logging.INFO)

import math
from pathlib import Path
from pyglm import glm
import moderngl
import moderngl_window as mglw
from moderngl_window.scene import Scene
from moderngl_window.context.headless import Window as HeadlessWindow
from moderngl_window.resources import scenes
from moderngl_window.meta import SceneDescription
import numpy as np


class ThreeDimModel(BaseWidget):
    name = '3D model'

    config_definition = {
        'orientation_x': config_types.DataPoint(),
        'orientation_y': config_types.DataPoint(),
        'orientation_z': config_types.DataPoint(),
        'model': config_types.File(),
        'max_framerate': config_types.Int(default=60),
        'distance': config_types.Float(default=1),
        'resolution': config_types.Group({
            'width': config_types.Int(default=512),
            'height': config_types.Int(default=512)
        })
    }

    wnd: Optional[HeadlessWindow] = None
    scene: Optional[mglw.scene.Scene] = None
    proj: Optional[glm.mat4x4] = None
    camera: Optional[glm.mat4x4] = None
    fbo: Optional[moderngl.Framebuffer] = None

    def __init__(self, *args):
        super(ThreeDimModel, self).__init__(*args)

        self.logger.info('init')

        """if self.config['orientation_x'] == '':
            return
        if self.config['orientation_y'] == '':
            return
        if self.config['orientation_z'] == '':
            return"""

        h = self.config['resolution']['height']
        w = self.config['resolution']['width']
        with dpg.texture_registry():
            self.texture = dpg.add_raw_texture(
                width=w,
                height=h,
                default_value=[0] * w * h,  # fill with 0 (black pixels)
                format=dpg.mvFormat_Float_rgb
            )
        self.image = dpg.add_image(parent=self.window, texture_tag=self.texture, width=w, height=h)


    def init_3d(self):
        h = self.config['resolution']['height']
        w = self.config['resolution']['width']

        self.wnd = HeadlessWindow(size=(w, h))
        mglw.activate_context(ctx=self.wnd.ctx)

        self.logger.info(f'Using model {self.config['model']}')

        resource_dir = Path(self.config['model']).parent.resolve()
        mglw.resources.register_scene_dir(resource_dir)
        self.scene = scenes.load(SceneDescription(path=Path(self.config['model']).name))

        center = self.scene.get_center()
        self.proj = glm.perspective(glm.radians(75.0), w / h, 0.1, 1000.0)
        self.camera = glm.lookAt(
            center + glm.vec3(math.sin(90) * self.scene.diagonal_size*self.config['distance'], 0.0, self.scene.diagonal_size*self.config['distance']),
            center,
            glm.vec3(0.0, 1.0, 0.0),
        )

        self.fbo = self.wnd.ctx.framebuffer(
            color_attachments=[self.wnd.ctx.texture((w, h), 3)],
            depth_attachment=self.wnd.ctx.depth_renderbuffer((w, h)),
        )

    i = 0
    last_frame_t = 0
    def render(self):
        if self.config['model'] == '':
            return
        """if self.config['orientation_x'] == '':
            return
        if self.config['orientation_y'] == '':
            return
        if self.config['orientation_z'] == '':
            return

        orientation_x = Data.plugin.dictionary[self.config['orientation_x']]
        orientation_y = Data.plugin.dictionary[self.config['orientation_y']]
        orientation_z = Data.plugin.dictionary[self.config['orientation_z']]"""

        if time.monotonic() - self.last_frame_t < 1/self.config['max_framerate']:
            return
        self.last_frame_t = time.monotonic()

        if self.wnd is None:
            self.init_3d()

        self.i += 1
        rx = glm.rotate(glm.radians(self.i), glm.vec3(1, 0, 0))
        ry = glm.rotate(glm.radians(self.i), glm.vec3(0, 1, 0))
        rz = glm.rotate(glm.radians(self.i), glm.vec3(0, 0, 1))
        self.scene.matrix = rz * ry * rx

        self.fbo.use()
        self.wnd.ctx.clear(37/255, 37/255, 38/255)
        self.wnd.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        self.scene.draw(
            projection_matrix=self.proj,
            camera_matrix=self.camera,
            time=0.0,
        )

        raw = self.fbo.color_attachments[0].read()
        img = np.frombuffer(raw, dtype="u1").reshape(self.config['resolution']['height'], self.config['resolution']['width'], 3)

        #frame = cv2.resize(frame, (width, height))
        frame_1d = np.flipud(img).ravel()  # flatten camera data to a 1d structure
        frame_float = np.asarray(frame_1d, dtype='f')  # change data type to float
        data = np.true_divide(frame_float, 255)  # normalize pixels

        dpg.set_value(self.texture, data)  # update texture
