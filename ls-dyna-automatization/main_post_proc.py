from pre_proc import ls_c_runner as ls
from post_proc import post_proc_picture_gen as pppg
from post_proc import post_proc_stl_gen as ppsg
from post_proc import post_proc_curv_gen as ppcg
from post_proc import file_copy as fc

if __name__ == "__main__":
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
    for folder in FH.k_file_folders:
        png_path = CFPM.c_file_manipulation(folder)
        KFG.lsrun_command_runner(CFPM.new_c_file_path)
        CFSM.c_file_manipulation(folder)
        KFG.lsrun_command_runner(CFSM.new_c_file_path)
        PVCG.main(folder)
        FC.file_copy(png_path, sim_png)
