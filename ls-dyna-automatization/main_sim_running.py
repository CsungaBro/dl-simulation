from pre_proc import geom_gen as gg
from pre_proc import ls_c_runner as ls
from pre_proc import my_sql_handler as sql_h
from logger import csu_logger as csu_logger
import os
import shutil


class InformationHandler:
    def __init__(self) -> None:
        pass


class DirHandler:
    def __init__(self, k_folder, c_folder) -> None:
        self.k_folder = os.path.abspath(k_folder)
        self.c_folder = os.path.abspath(c_folder)
        # self.dir_cleaner()
        # self.dir_maker()
    
    def dir_maker(self):
        for folder in [self.k_folder, self.c_folder]:
            os.makedirs(folder)

    def dir_cleaner(self):
        for folder in [self.k_folder, self.c_folder]:
            if os.path.exists(folder):
                shutil.rmtree(folder)


class ScriptRunner:
    """This part gets the diffent commponent togother and runs them"""
    def __init__(self, number_of_files, FileHandler, SimulationGenerator):
        self.number_of_files = number_of_files
        self.FileHandler = FileHandler
        self.SimulationGenerator = SimulationGenerator
    
    def script_running(self):
        for files in range(self.number_of_files):
            paths = self.FileHandler.files_preper()
            c_file_path, k_file_path = paths[0], paths[1]
            self.SimulationGenerator.lsrun_command_maker(k_file_path)
            logger.info("KFile {} is generated".format(files))
        self.SimulationGenerator.lsrun_command_runner()


if __name__ == "__main__":
    logger = csu_logger.logger_init()
    IH = InformationHandler()
    IH.c_dir_path = "output\\c_files"    
    IH.k_dir_path = "output\\k_files"
    IH.current_path = "C:\\Users\\CsungaBro\\Documents\\code\\server-test"

    DH = DirHandler(IH.k_dir_path, IH.c_dir_path)

    # ONG = gg.OutputNameGenerator(IH.c_dir_path, IH.all_parameters_container)
    # ONG.output_path_generator()
    # IH.output_names = ONG.output_names

    FH = ls.FileHandler(IH.c_dir_path, IH.k_dir_path)
    SG = ls.SimulationGenerator()
    SC = ScriptRunner(FH.c_files_to_prep, FH, SG)
    SC.script_running()