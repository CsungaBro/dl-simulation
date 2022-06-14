from pre_proc import geom_gen as gg
from pre_proc import ls_c_runner as ls
from pre_proc import my_sql_handler as sql_h
from logger import csu_logger as csu_logger
import os
import shutil


class InformationHandler:
    def __init__(self) -> None:
        pass

        # self.height_range
        # self.radius_range
        # self.number_of_simulation
        # self.c_dir_path
        # self.c_file_template_path
        # self.k_dir_path
        # self.c_file_save_path


class DirHandler:
    def __init__(self, k_folder, c_folder) -> None:
        self.k_folder = os.path.abspath(k_folder)
        self.c_folder = os.path.abspath(c_folder)
        self.dir_cleaner()
        self.dir_maker()
    
    def dir_maker(self):
        for folder in [self.k_folder, self.c_folder]:
            os.makedirs(folder)

    def dir_cleaner(self):
        for folder in [self.k_folder, self.c_folder]:
            if os.path.exists(folder):
                shutil.rmtree(folder)


class ParamaterTextGenerator:
    def __init__(self, container) -> None:
        self.path = "misc\\parameter_text.txt"
        self.p_container = container

    def generate_text_file(self):
        with open(self.path, "w") as ft:
            ft.write(f"key           =     value\n")
            for count, files in enumerate(self.p_container):
                ft.write(f"File:{count:2}.-----------------\n")
                for key, value in files.items():
                    ft.write(f"{key:13} = {value:9}\n")


class ScriptRunner:
    """This part gets the diffent commponent togother and runs them"""
    def __init__(self, number_of_files, FileHandler, KFileGenerator, KFileSaveHandling, SimulationGenerator, CFileManipulator ):
        self.number_of_files = number_of_files
        self.FileHandler = FileHandler
        self.KFileGenerator = KFileGenerator
        self.KFileSaveHandling = KFileSaveHandling
        self.SimulationGenerator = SimulationGenerator
        self.CFileManipulator = CFileManipulator
    
    def script_running(self):
        for files in range(self.number_of_files):
            paths = self.FileHandler.files_preper()
            c_file_path, k_file_path = paths[0], paths[1]
            self.CFileManipulator.c_file_save_adder(c_file_path, k_file_path)
            self.KFileGenerator.lsrun_command_runner(c_file_path)
            self.KFileSaveHandling.generate_give_k_file(k_file_path, files)
            self.SimulationGenerator.lsrun_command_maker(k_file_path)
            print("KFile {} is generated".format(files))
        self.SimulationGenerator.lsrun_command_runner()

if __name__ == "__main__":
    logger = csu_logger.logger_init()
    IH = InformationHandler()
    IH.height_range = [5,30]
    IH.radius_range = [2,20]
    IH.number_of_simulation = 10
    IH.c_dir_path = "output\\c_files"
    IH.k_dir_path = "output\\k_files"
    IH.c_file_template_path = "template\\save_2.cfile"
    IH.c_file_save_path = "template\\save_temp.cfile"
    IH.db_name = "Test_Paramaters"
    IH.table_name = "test_parameters"
    IH.pkl_path = 'template\\test.pkl'

    DH = DirHandler(IH.k_dir_path, IH.c_dir_path)

    # mysql_handler = sql_h.MySQLHandler(IH.db_name, IH.table_name)

    P = gg.GeometricParameters(IH.pkl_path, IH.number_of_simulation)
    # P = gg.GeometricParameters(IH.pkl_path, 10)
    P.generate_all_parameters()
    IH.all_parameters_container = P.all_parameters_container

    PTG = ParamaterTextGenerator(P.all_parameters_container)
    PTG.generate_text_file()

    ONG = gg.OutputNameGenerator(IH.c_dir_path, IH.all_parameters_container)
    ONG.output_path_generator()
    IH.output_names = ONG.output_names

    CFH = gg.CFileHandling(IH.c_file_template_path, IH.all_parameters_container, IH.output_names)
    CFH.generate_all_c_file()

    FH = ls.FileHandler(IH.c_dir_path, IH.k_dir_path)
    CFM = ls.CFileManipulator(IH.c_file_save_path)
    KFG = ls.KFileGenerator()
    KFH = gg.KFileSaveHandling(P.all_parameters_container, ONG.output_names)
    SG = ls.SimulationGenerator()

    SC = ScriptRunner(FH.c_files_to_prep, FH, KFG, KFH, SG, CFM)
    SC.script_running()