from regex import W
from pre_proc import ls_c_runner as ls
from post_proc import post_proc_picture_gen as pppg
from post_proc import post_proc_stl_gen as ppsg
from post_proc import post_proc_curv_gen as ppcg
from post_proc import file_copy as fc
import numpy as np


if __name__ == "__main__":
    # folder = 'output\\k_files\\sim_7546_80.0x80.0x11.73_R7.36'
    # folder = 'output\\k_files\\sim_1087_25.45x63.64x15.27_R8.45'
    folder = 'output\\k_files\\sim_287_20.0x47.27x15.27_R7.36'

    k_dir_path = "output\\k_files"
    c_file_png_template_path = "template\\image_gen.cfile"
    c_file_stl_template_path = "template\\stl_gen.cfile"
    sim_png = "output\\sim"

    FH = pppg.FileHandler(k_dir_path, c_file_png_template_path)
    CFPM = pppg.CFilePngManipulator(c_file_png_template_path)
    CFSM = ppsg.CFileSTLManipulator(c_file_stl_template_path)
    KFG = ls.KFileGenerator()
    PVCG = ppcg.PyVistaCurvatureGenerator()
    FC = fc.FileCopy()
    png_path = CFPM.c_file_manipulation(folder)
    KFG.lsrun_command_runner(CFPM.new_c_file_path)
    CFSM.c_file_manipulation(folder)
    KFG.lsrun_command_runner(CFSM.new_c_file_path)
    PVCG.main(folder)
    FC.file_copy(png_path, sim_png)    
    curv_generator = ppcg.PyVistaCurvatureGenerator()
    curv_generator.main(folder)
    camera_pos = curv_generator.plotter.camera_position
    print(camera_pos)
    with open("camera_pos_test_2.txt", "w") as fw:
        for row in camera_pos:
            h1 = str(row[0])
            h2 = str(row[1])
            h3 = str(row[2])
            fw.write(f"{h1},{h2},{h3}\n")
    t = []
    with open("camera_pos_test_2.txt", "r") as fr:
        for line in fr:
            h1 = line.split(",")
            print(h1)
            h2 = (float(h1[0]), float(h1[1]), float(h1[2]))
            t.append(h2)
    print(t)