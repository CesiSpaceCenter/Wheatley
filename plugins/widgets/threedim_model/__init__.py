import dearpygui.dearpygui as dpg

from plugins.base_widget import BaseWidget
from plugins.config_ui import config_types
from plugins.data import Data

import numpy as np
import pyrender
import trimesh
import numpy as np


class ThreeDimModel(BaseWidget):
    name = '3D model'

    config_definition = {
        'orientation_x': config_types.DataPoint(),
        'orientation_y': config_types.DataPoint(),
        'orientation_z': config_types.DataPoint()
    }

    def __init__(self, *args):
        super(ThreeDimModel, self).__init__(*args)

        """if self.config['orientation_x'] == '':
            return
        if self.config['orientation_y'] == '':
            return
        if self.config['orientation_z'] == '':
            return"""

        self.texture = dpg.add_raw_texture(
            parent=self.window,
            width=512,
            height=512,
            default_value=[0] * 512 * 512,  # fill with 0 (black pixels)
            format=dpg.mvFormat_Float_rgb
        )
        self.image = dpg.add_image(parent=self.window, texture_tag=self.texture, width=512, height=512)

        mesh_trimesh = trimesh.load("model.gltf")
        mesh = pyrender.Mesh.from_trimesh(mesh_trimesh)

        self.scene = pyrender.Scene()

        # ajouter mesh et garder le node
        self.node = self.scene.add(mesh)

        camera = pyrender.PerspectiveCamera(yfov=np.pi / 3)
        camera_pose = np.eye(4)
        camera_pose[2, 3] = 2
        self.scene.add(camera, pose=camera_pose)

        light = pyrender.DirectionalLight(color=np.ones(3), intensity=3)
        self.scene.add(light, pose=camera_pose)

        self.renderer = pyrender.OffscreenRenderer(512, 512)

    i = 0
    def render(self):
        """if self.config['orientation_x'] == '':
            return
        if self.config['orientation_y'] == '':
            return
        if self.config['orientation_z'] == '':
            return

        orientation_x = Data.plugin.dictionary[self.config['orientation_x']]
        orientation_y = Data.plugin.dictionary[self.config['orientation_y']]
        orientation_z = Data.plugin.dictionary[self.config['orientation_z']]"""

        angle = self.i * 2 * np.pi / 60
        self.i += 1

        pose = trimesh.transformations.rotation_matrix(
            angle,
            [0, 0, 1]
        )

        # mettre à jour la pose
        self.scene.set_pose(self.node, pose)

        color, depth = self.renderer.render(self.scene)

        #frame = cv2.resize(frame, (width, height))
        frame_1d = color.ravel()  # flatten camera data to a 1d structure
        frame_float = np.asarray(frame_1d, dtype='f')  # change data type to float
        data = np.true_divide(frame_float, 255)  # normalize pixels

        dpg.set_value(self.texture, data)  # update texture
