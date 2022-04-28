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

    def curvature_generation(self, output_path) -> None:
        self.plotter = pv.Plotter(off_screen=True)
        self.plotter.background_color = (0,0,0)
        print(self.stl_path)
        mesh = pv.read(self.stl_path)
        curv = mesh.curvature(curv_type="mean")
        mesh_actor = self.add_actor_to_plotter(mesh, curv)
        self.plotter.view_xy()        
        self.plotter.show(screenshot=output_path)
        self.remove_actor_to_plotter(mesh_actor)

    def add_actor_to_plotter(self, mesh, curv) -> object:
        mesh_actor = self.plotter.add_mesh(mesh, scalars=curv, clim=[-0.35, 0],  cmap="gray", lighting=False)
        # mesh_actor = self.plotter.add_mesh(mesh, scalars=curv,  cmap="gray", lighting=False)
    
    def remove_actor_to_plotter(self, actor):
        self.plotter.remove_actor(actor)