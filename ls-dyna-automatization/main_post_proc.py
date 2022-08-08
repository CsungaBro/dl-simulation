from tracemalloc import start
from pre_proc import ls_c_runner as ls
from post_proc import post_proc_picture_gen as pppg
from post_proc import post_proc_stl_gen as ppsg
from post_proc import post_proc_curv_gen as ppcg
from post_proc import file_copy as fc
from logger import csu_logger
import time

if __name__ == "__main__":
    k_dir_path = "output\\k_files"
    c_file_png_template_path = "template\\image_gen.cfile"
    c_file_stl_template_path = "template\\stl_gen.cfile"
    sim_png = "output\\sim"

    logger = csu_logger.logger_init()

    FH = pppg.FileHandler(k_dir_path, c_file_png_template_path)
    CFPM = pppg.CFilePngManipulator(c_file_png_template_path)
    CFSM = ppsg.CFileSTLManipulator(c_file_stl_template_path)
    KFG = ls.KFileGenerator()
    PVCG = ppcg.PyVistaCurvatureGenerator()
    FC = fc.FileCopy()
    start_time = time.time()
    k_folder_number = len(FH.k_file_folders)
    for count, folder in enumerate(FH.k_file_folders):
        loop_start_time = time.time()
        png_path = CFPM.c_file_manipulation(folder)
        KFG.lsrun_command_runner(CFPM.new_c_file_path)
        CFSM.c_file_manipulation(folder)
        KFG.lsrun_command_runner(CFSM.new_c_file_path)
        PVCG.main(folder)
        FC.file_copy(png_path, sim_png)
        run_time = time.time() - start_time
        run_time_str = time.strftime('%H:%M:%S', time.gmtime(int(run_time)))
        loop_time = time.time() - loop_start_time
        processed = count + 1
        full_time_est = (run_time / processed)*k_folder_number
        full_time_str = time.strftime('%H:%M:%S', time.gmtime(int(full_time_est)))
        logger.info(f"Processed: {processed} / {k_folder_number}\nRuntime:{run_time_str}\nLooptime:{loop_time:.2f}\nEstimated runtime:{full_time_str} ")