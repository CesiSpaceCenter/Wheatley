import logging

logging.getLogger('moderngl_window').setLevel(logging.INFO)
import math
import threading
from queue import Queue, Empty
import time
from pathlib import Path
from typing import Optional
import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data

from pyglm import glm
import moderngl
import moderngl_window as mglw
import numpy as np


class ThreeDimModel(BaseWidget):
    name = '3D model'

    config_definition = {
        'orientation_x': config_types.DataPoint(),
        'orientation_y': config_types.DataPoint(),
        'orientation_z': config_types.DataPoint(),
        'model': config_types.File(default=r'C:\Users\epuiroux\Documents\dev\Wheatley\model.gltf'),
        'max_framerate': config_types.Int(default=60),
        'distance': config_types.Float(default=1),
        'resolution': config_types.Group({
            'width': config_types.Int(default=512),
            'height': config_types.Int(default=512)
        })
    }

    gl_run = True

    thread: Optional[threading.Thread] = None
    queue: Optional[Queue] = None

    def __init__(self, *args):
        super(ThreeDimModel, self).__init__(*args)

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

        if self.config['model'] == '':
            return

    def gl_render(self):
        h = self.config['resolution']['height']
        w = self.config['resolution']['width']
        # wnd = HeadlessWindow(size=(w, h))
        # self.ctx = wnd.ctx

        ctx = moderngl.create_standalone_context()
        mglw.activate_context(ctx=ctx)

        self.logger.info(f'Using model {self.config['model']}')

        resource_dir = Path(self.config['model']).parent.resolve()
        mglw.resources.register_scene_dir(resource_dir)
        scene = mglw.resources.scenes.load(mglw.meta.SceneDescription(path=Path(self.config['model']).name))

        center = scene.get_center()
        proj = glm.perspective(glm.radians(75.0), w / h, 0.1, 1000.0)
        camera = glm.lookAt(
            center + glm.vec3(math.sin(90) * scene.diagonal_size * self.config['distance'], 0.0,
                              scene.diagonal_size * self.config['distance']),
            center,
            glm.vec3(0.0, 1.0, 0.0),
        )

        fbo = ctx.framebuffer(
            color_attachments=[ctx.texture((w, h), 3)],
            depth_attachment=ctx.depth_renderbuffer((w, h)),
        )

        i = 0
        last_frame_t = 0
        while self.gl_run:
            """if self.config['orientation_x'] == '':
                return
            if self.config['orientation_y'] == '':
                return
            if self.config['orientation_z'] == '':
                return
    
            orientation_x = Data.plugin.dictionary[self.config['orientation_x']]
            orientation_y = Data.plugin.dictionary[self.config['orientation_y']]
            orientation_z = Data.plugin.dictionary[self.config['orientation_z']]"""

            if time.monotonic() - last_frame_t < 1/self.config['max_framerate']:
                continue
            last_frame_t = time.monotonic()

            i += 1
            rx = glm.rotate(glm.radians(i), glm.vec3(1, 0, 0))
            ry = glm.rotate(glm.radians(i), glm.vec3(0, 1, 0))
            rz = glm.rotate(glm.radians(i), glm.vec3(0, 0, 1))
            scene.matrix = rz * ry * rx

            fbo.use()
            ctx.clear(37/255, 37/255, 38/255)
            ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
            scene.draw(
                projection_matrix=proj,
                camera_matrix=camera,
                time=0.0,
            )

            raw = fbo.color_attachments[0].read()
            # frame = cv2.resize(frame, (width, height))
            data = np.frombuffer(raw, dtype="u1").reshape(h, w, 3)
            frame_1d = np.flipud(data).ravel()  # flatten camera data to a 1d structure
            frame_float = np.asarray(frame_1d, dtype='f')  # change data type to float
            data = np.true_divide(frame_float, 255)  # normalize pixels
            #self.data = raw
            self.queue.put(data)

    def render(self):
        if self.config['model'] == '':
            return
        if self.thread is None:
            self.queue = Queue(maxsize=1)
            self.thread = threading.Thread(target=self.gl_render, daemon=True)
            self.thread.start()

        try:
            data = self.queue.get(block=False)
        except Empty:
            return

        dpg.set_value(self.texture, data)  # update texture

    def cleanup(self):
        self.gl_run = False
        if self.thread is not None:
            self.thread.join()
        if self.queue is not None and hasattr(self.queue, 'shutdown'):  # py >= 3.13
            self.queue.shutdown()