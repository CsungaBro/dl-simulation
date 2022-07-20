from regex import W
from pre_proc import ls_c_runner as ls
from post_proc import post_proc_picture_gen as pppg
from post_proc import post_proc_stl_gen as ppsg
from post_proc import post_proc_curv_gen as ppcg
from post_proc import file_copy as fc
import numpy as np
import pyvista as pv
import os
import regex as re

def adding_the_plot(path):
    mesh =pv.read(path)
    plotter = pv.Plotter(off_screen=True)
    plotter.background_color = (0,0,0)
    curv = mesh.curvature(curv_type="mean")
    mesh_actor = plotter.add_mesh(mesh, scalars=curv, clim=[-0.35, 0],  cmap="gray", lighting=False)
    plotter.view_xy()
    return plotter

def camera_pos_calc(a_1, b_1, a_2, b_2):
    x_1 = a_1/2-1
    y_1 = b_1/2-1

    x_2 = a_2/2-1
    y_2 = b_2/2-1

    dx_3 = abs(x_2-x_1)
    dy_3 = abs(y_2-y_1)  

    x_3 = x_2-dx_3*1
    y_3 = y_2-dy_3*1

    camera_pos = [
        (x_3, y_3, 260), 
        (x_3, y_3, 41), 
        (0.0, 1.0, 0.0)]

    return camera_pos

def size_getter(base_name):
    nums = re.findall("[0-9]+[.][0-9]+", base_name)
    return float(nums[0]), float(nums[1])

if __name__ == "__main__":
    folder_1 = 'output\\k_files\\sim_7546_80.0x80.0x11.73_R7.36'
    # folder = 'output\\k_files\\sim_1087_25.45x63.64x15.27_R8.45'
    folder_2 = 'output\\k_files\\sim_287_20.0x47.27x15.27_R7.36'

    name_1 = os.path.basename(folder_1)
    name_2 = os.path.basename(folder_2)
 

    a_1, b_1 = size_getter(name_1)
    a_2, b_2 = size_getter(name_2)
            
    camera_pos_3 = camera_pos_calc(a_1, b_1, a_2, b_2)

    k_dir_path = "output\\k_files"
    c_file_png_template_path = "template\\image_gen.cfile"
    c_file_stl_template_path = "template\\stl_gen.cfile"
    sim_png = "output\\sim"
    sim_name_1 = os.path.basename(folder_1)
    stl_name_1 = f"{sim_name_1}_stl_gen1_25.stl"
    stl_path_1 = os.path.join(folder_1, stl_name_1)
    plotter_1 = adding_the_plot(stl_path_1)
    plotter_1.remove_scalar_bar()
    plotter_1.screenshot("m1.jpg")
    plotter_1.show()

    sim_name_2 = os.path.basename(folder_2)
    stl_name_2 = f"{sim_name_2}_stl_gen1_25.stl"
    stl_path_2 = os.path.join(folder_2, stl_name_2)

    plotter_4 = adding_the_plot(stl_path_2)
    plotter_4.camera_position = camera_pos_3
    plotter_4.remove_scalar_bar()
    plotter_4.screenshot("m2.jpg")
    plotter_4.show()
    print(camera_pos_3)