from regex import W
from pre_proc import ls_c_runner as ls
from post_proc import post_proc_picture_gen as pppg
from post_proc import post_proc_stl_gen as ppsg
from post_proc import post_proc_curv_gen as ppcg
from post_proc import file_copy as fc
import numpy as np
import pyvista as pv
import os

def adding_the_plot(path):
    mesh =pv.read(path)
    plotter = pv.Plotter(off_screen=False)
    plotter.background_color = (0,0,0)
    curv = mesh.curvature(curv_type="mean")
    mesh_actor = plotter.add_mesh(mesh, scalars=curv, clim=[-0.35, 0],  cmap="gray", lighting=False)
    plotter.view_xy()
    return plotter

if __name__ == "__main__":
    folder_1 = 'output\\k_files\\sim_7546_80.0x80.0x11.73_R7.36'
    # folder = 'output\\k_files\\sim_1087_25.45x63.64x15.27_R8.45'
    folder_2 = 'output\\k_files\\sim_287_20.0x47.27x15.27_R7.36'

    camera_pos = [
            (39.0, 39.0, 258.5020178141234), 
            (39.0, 39.0, 40.959999084472656), 
            (0.0, 1.0, 0.0)]

    camera_pos_2 = [
            (40.0, 40.0, 260), 
            (40.0, 40.0, 41), 
            (0.0, 1.0, 0.0)]

    a_1 = 80.0
    b_1 = 80.0    

    a_2 = 20.0
    b_2 = 47.27    

    x_1 = a_1/2-1
    y_1 = b_1/2-1

    x_2 = a_2/2-1
    y_2 = b_2/2-1

    dx_3 = abs(x_2-x_1)
    dy_3 = abs(y_2-y_1)

    print(f"dx_3:{dx_3}")    
    print(f"dy_3:{dy_3}")    

    x_3 = x_2-dx_3*1
    y_3 = y_2-dy_3*1

    x_4 = -20
    y_4 = 6.2

    camera_pos_4 = [
        (x_1, y_1, 260), 
        (x_1, y_1, 41), 
        (0.0, 1.0, 0.0)]

    camera_pos_3 = [
            (y_3, x_3, 260), 
            (y_3, x_3, 41), 
            (0.0, 1.0, 0.0)]

    camera_pos_5 = [
            (y_2, x_2, 260), 
            (y_2, x_2, 41), 
            (0.0, 1.0, 0.0)]

    camera_pos_6 = [
            (x_4, y_4, 260), 
            (x_4, y_4, 41), 
            (0.0, 1.0, 0.0)]

    print(camera_pos_2)
    print(camera_pos_3)
    k_dir_path = "output\\k_files"
    c_file_png_template_path = "template\\image_gen.cfile"
    c_file_stl_template_path = "template\\stl_gen.cfile"
    sim_png = "output\\sim"
    sim_name_1 = os.path.basename(folder_1)
    stl_name_1 = f"{sim_name_1}_stl_gen1_25.stl"
    stl_path_1 = os.path.join(folder_1, stl_name_1)
    plotter_1 = adding_the_plot(stl_path_1)
    plotter_1.show()

    plotter_1_cam_post = plotter_1.camera.position 
    print(plotter_1_cam_post)

    plotter_4 = adding_the_plot(stl_path_1)
    plotter_4.camera_position = camera_pos_4
    plotter_4.show()

    # plotter_5 = adding_the_plot(stl_path_1)
    # plotter_5.set_viewup([0,1,0])
    # plotter_5.show()

    sim_name_2 = os.path.basename(folder_2)
    stl_name_2 = f"{sim_name_2}_stl_gen1_25.stl"
    stl_path_2 = os.path.join(folder_2, stl_name_2)
    plotter_2 = adding_the_plot(stl_path_2)
    plotter_2.show()

    # plotter_2_cam_post = plotter_2.camera_position
    # print(plotter_2_cam_post)

    plotter_3 = adding_the_plot(stl_path_2)
    plotter_3.camera_position = camera_pos_5
    plotter_3.remove_scalar_bar()
    plotter_3.show()

    plotter_4 = adding_the_plot(stl_path_2)
    plotter_4.camera_position = camera_pos_4
    plotter_4.remove_scalar_bar()
    plotter_4.show()
    print(camera_pos_4)

    plotter_4 = adding_the_plot(stl_path_2)
    plotter_4.camera_position = camera_pos_3
    plotter_4.remove_scalar_bar()
    plotter_4.show()
    print(camera_pos_3)

    plotter_4 = adding_the_plot(stl_path_2)
    plotter_4.camera_position = camera_pos_6
    plotter_4.remove_scalar_bar()
    plotter_4.show()
    print(camera_pos_6)    

    # plotter_2_cam_post = plotter_3.camera_position
    # print(plotter_2_cam_post)    