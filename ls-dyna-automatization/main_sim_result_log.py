from pre_proc import ls_c_runner as ls
from logger import csu_logger as csu_logger
import os
import shutil


class InformationHandler:
    def __init__(self) -> None:
        pass


class DirFileHandler:
    def __init__(self, new_folder_path) -> None:
        self.new_folder_path = new_folder_path
    
    def dir_maker(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def file_copy(self, new_k_dir_path, og_k_file_path, file_name):
        og_k_dir_path = os.path.dirname(og_k_file_path)
        new_k_file_path = os.path.join(new_k_dir_path, file_name)
        new_d3plot_path = os.path.join(new_k_dir_path, 'd3plot')
        new_d3plot1_path = os.path.join(new_k_dir_path, 'd3plot01')
        new_d3plot2_path = os.path.join(new_k_dir_path, 'd3plot02')
        og_d3plot_path =os.path.join(og_k_dir_path, 'd3plot')
        og_d3plot1_path =os.path.join(og_k_dir_path, 'd3plot01')
        og_d3plot2_path =os.path.join(og_k_dir_path, 'd3plot02')
        og_files_paths = [og_k_file_path, og_d3plot_path, og_d3plot1_path, og_d3plot2_path]
        new_files_paths = [new_k_file_path, new_d3plot_path, new_d3plot1_path, new_d3plot2_path]
        for old_file_path, new_file_path in zip(og_files_paths, new_files_paths):
            shutil.copy(old_file_path, new_file_path)    


    def file_manager(self, og_k_file_path):
        file_name = os.path.basename(og_k_file_path)
        new_k_dir_path = os.path.join(self.new_folder_path, file_name[:-2])
        self.dir_maker(new_k_dir_path)
        self.file_copy(new_k_dir_path, og_k_file_path, file_name)


class ScriptRunner:
    """This part gets the diffent commponent togother and runs them"""
    def __init__(self, number_of_files, FileHandler, DirFileHandler):
        self.number_of_files = number_of_files
        self.FileHandler = FileHandler
        self.DirFileHandler = DirFileHandler
    
    def script_running(self):
        for files in range(self.number_of_files):
            paths = self.FileHandler.files_preper()
            c_file_path, k_file_path = paths[0], paths[1]
            self.DirFileHandler.file_manager(k_file_path)
            logger.info("KFile {} is copied to the folder".format(os.path.basename(k_file_path)[:-2]))


if __name__ == "__main__":
    logger = csu_logger.logger_init()
    IH = InformationHandler()
    IH.c_dir_path = "output\\c_files"    
    IH.k_dir_path = "output\\k_files"
    IH.current_path = "C:\\Users\\CsungaBro\\Documents\\code\\server-test"
    IH.new_k_dir_path = "exp\\k_files"

    DFH = DirFileHandler(IH.new_k_dir_path)

    # ONG = gg.OutputNameGenerator(IH.c_dir_path, IH.all_parameters_container)
    # ONG.output_path_generator()
    # IH.output_names = ONG.output_names

    FH = ls.FileHandler(IH.c_dir_path, IH.k_dir_path)
    SC = ScriptRunner(FH.c_files_to_prep, FH, DFH)
    SC.script_running()