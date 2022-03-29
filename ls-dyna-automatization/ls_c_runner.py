import subprocess
import os
import regex as re 


class FileHandler:
    def __init__(self, c_file_folder_path, k_file_folder_path):
        self.c_file_folder_path = c_file_folder_path
        self.k_file_folder_path = k_file_folder_path
        self.c_files_processed = 0
        self.c_files = self.c_file_reader()
        self.c_files_to_prep = len(self.c_files)

    def c_file_reader(self):
        return os.listdir(self.c_file_folder_path)

    def files_preper(self):
        c_file_path = os.path.join(self.c_file_folder_path, self.c_files[self.c_files_processed])
        k_file_name =re.sub("cfile$", "k", self.c_files[self.c_files_processed])
        k_file_path = os.path.join(self.k_file_folder_path, k_file_name)
        self.c_files_processed += 1
        print(c_file_path, k_file_path)
        return c_file_path, k_file_path


class PowershellRunner:
    def __init__(self):
        self.lspp_powershell_env_path = "D:\\Program Files\\ANSYS 2020R2 LS-DYNA Student 12.0.0\\LS-DYNA\\env.ps1"

    def command_runner(self, c_file_path, k_file_path):
        print(c_file_path, c_file_path)        
        print(k_file_path, k_file_path)  

    def fafo(self, c_file_path: str):
        print("FAFO")
        print(c_file_path)
        completed = subprocess.run(["powershell", "-Command", c_file_path], capture_output=True)
        


class ScriptRunner:
    def __init__(self, number_of_files, FileHandler, PowershellRunner ):
        self.number_of_files = number_of_files
        self.FileHandler = FileHandler
        self.PowershellRunner = PowershellRunner
    
    def k_file_generator(self):
        for files in range(self.number_of_files):

            print("\n")
            print(self.FileHandler.files_preper())
            print("\n")

            self.PowershellRunner.command_runner(self.FileHandler.files_preper())


if __name__ == "__main__":
    # c_files_path = "output\c_files"
    # k_files_path = "output\k_files"
    # FH = FileHandler(c_files_path, k_files_path)
    PR = PowershellRunner()
    # SC = ScriptRunner(FH.c_files_to_prep, FH, PR)
    # SC.k_file_generator()
    
    PR.fafo("output\\c_files\\test.cfile")