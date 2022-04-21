from pre_proc import ls_c_runner as ls
from post_proc import post_proc_picture_gen as pppg

if __name__ == "__main__":
    k_dir_path = "output\\k_files"
    c_file_template_path = "template\image_gen.cfile"

    FH = pppg.FileHandler(k_dir_path, c_file_template_path)
    CFM = pppg.CFileManipulator(c_file_template_path)
    KFG = ls.KFileGenerator()
    for folder in FH.k_file_folders:
        CFM.c_file_manipulation(folder)
        KFG.lsrun_command_runner(CFM.new_c_file_path)