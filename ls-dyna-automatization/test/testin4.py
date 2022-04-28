# import os
# import pymesh
# import plotly.graph_objects as go
# import pyvista as pv
# from meshplot import plot, subplot, interact, offline


# # mesh_path = "test\Torus.stl"
# mesh_path = "output\k_files\sim_0_120x120x27.5_R6.5\sim_0_120x120x27.5_R6.5_stl_gen1_25.stl"
# # mesh_path = "output\k_files\sim_0_120x120x27.5_R6.5\sim_0_120x120x27.5_R6.5_stl_gen2_25.stl"


# mesh = pv.read(mesh_path)
# curv = mesh.curvature(curv_type="Mean")
# # curv = mesh.curvature(curv_type="Gaussian")
# plotter = pv.Plotter(off_screen=True)
# # # plotter.camera_position = 'yx'
# # # plotter.set_focus(mesh.center)
# # # plotter.camera_set = True
# # # plotter.add_mesh(mesh, scalars=curv, clim=[0, .05], cmap="gray", lighting=False)
# # # plotter.add_mesh(mesh, scalars=curv, clim=[-0.5, 0], cmap="gray", lighting=False)
# plotter.add_mesh(mesh, scalars=curv,  cmap="gray", lighting=False)
# plotter.background_color = (0,0,0)
# plotter.view_xy()
# plotter.show(screenshot='test.png')

# # import pyvista as pv
# # import numpy as np

# # mesh = pv.read(mesh_path)
# # curv = mesh.curvature(curv_type="mean")
# # curv = mesh.curvature(curv_type="gaussian")
# # mesh["gaussian_curvature"] = curv

# # cmin = np.percentile(curv, 00)
# # cmax = np.percentile(curv, 100)
# # print(cmin, cmax)
# # mesh.plot(scalars="gaussian_curvature", 
# #           cmap="jet", clim=[cmin,  cmax], cpos="xy")

# from post_proc import post_proc_curv_gen as ppcg

# folder_path = 'output\k_files\sim_0_120x120x27.5_R6.5'
# PVCG = ppcg.PyVistaCurvatureGenerator()
# PVCG.main(folder_path)