import pyvista as pv
import numpy as np
import regex as re
import os
from abc import ABC, abstractclassmethod


class CurvatureGenerator(ABC):
    def __init__(self, method='mean') -> None:
        self.method = method # mean / gaussian

    @abstractclassmethod
    def curvature_generation(self, output_path) -> None:
        pass

    def path_generator(self, folder):
        sim_name = os.path.basename(folder)
        stl_name = f"{sim_name}_stl_gen1_25.stl"
        output_name = f"{sim_name}_stl_gen1_25.png"
        self.stl_path = os.path.join(folder, stl_name)
        self.output_path = os.path.join(folder, output_name)
        self.curv_path = os.path.join("output\\curv", output_name)

    def main(self, folder):
        self.path_generator(folder)
        self.curvature_generation(self.output_path)
        self.curvature_generation(self.curv_path)


class PyVistaCurvatureGenerator(CurvatureGenerator):
    def __init__(self, method='mean') -> None:
        super().__init__(method)
        self.a_1 = 80
        self.b_1 = 80

    def size_getter(self, base_name):
        nums = re.findall("[0-9]+[.][0-9]+", base_name)
        return float(nums[0]), float(nums[1])

    def camera_pos_calc(self, a_2, b_2):
        #camera pos_bas
        x_1 = self.a_1/2-1
        y_1 = self.b_1/2-1
        #camera pos new
        x_2 = a_2/2-1
        y_2 = b_2/2-1
        #delta between the positions
        dx_3 = abs(x_2-x_1)
        dy_3 = abs(y_2-y_1)  
        # new cam pos
        x_3 = x_2-dx_3*1
        y_3 = y_2-dy_3*1
        return [
            (x_3, y_3, 260), 
            (x_3, y_3, 41), 
            (0.0, 1.0, 0.0)]

    def curvature_generation(self, output_path) -> None:
        self.plotter = pv.Plotter(off_screen=True)
        self.plotter.background_color = (0,0,0)
        # print(self.stl_path)
        mesh = pv.read(self.stl_path)
        curv = mesh.curvature(curv_type="mean")
        mesh_actor = self.add_actor_to_plotter(mesh, curv)
        self.plotter.view_xy()
        file_name =os.path.basename(self.stl_path)
        a_2, b_2 = self.size_getter(file_name)
        self.plotter.camera_position = self.camera_pos_calc(a_2, b_2)        
        self.plotter.remove_scalar_bar()
        self.plotter.show(screenshot=output_path)
        self.remove_actor_to_plotter(mesh_actor)

    def add_actor_to_plotter(self, mesh, curv) -> object:
        mesh_actor = self.plotter.add_mesh(mesh, scalars=curv, clim=[-0.35, 0],  cmap="gray", lighting=False)
        # mesh_actor = self.plotter.add_mesh(mesh, scalars=curv,  cmap="gray", lighting=False)
    
    def remove_actor_to_plotter(self, actor):
        self.plotter.remove_actor(actor)