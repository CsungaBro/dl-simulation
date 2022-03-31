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
        self.folder_maker()

    def c_file_reader(self):
        return os.listdir(self.c_file_folder_path)

    def files_preper(self):
        c_file_path = os.path.join(self.c_file_folder_path, self.c_files[self.c_files_processed])
        k_dir_name =re.sub(".cfile$", "", self.c_files[self.c_files_processed])
        k_file_name = "{}.k".format(k_dir_name)
        k_file_path = os.path.join(self.k_file_folder_path, k_dir_name,k_file_name)
        # try:
        #     k_file_folder =os.makedirs()
        # except:
        #     print("OH NO")
        self.c_files_processed += 1
        return c_file_path, k_file_path
    
    def folder_maker(self):
        c_file_path = os.path.join(self.c_file_folder_path, self.c_files[self.c_files_processed])
        for file in self.c_files:
            k_dir = os.path.join(self.k_file_folder_path, re.sub(".cfile$", "", file))
            if not os.path.exists(k_dir):
                os.mkdir(k_dir)


class FileManipulator:
    def __init__(self, save_part):
        self.save_part = save_part

    def c_file_save_adder(self, c_file, k_file):
        with open(c_file,"a") as fr, open(self.save_part, "r") as fs:
            for line in fs:
                if bool(re.search("path", line)):
                    k_file_full_path = os.path.abspath(k_file)
                    new_line = r'save keyword "{}"'.format(k_file_full_path)
                    fr.writelines(new_line)
                else:
                    fr.writelines(line)


class PowershellRunner:
    def __init__(self):
        self.lspp_powershell_env_path = "D:\\Program Files\\ANSYS 2020R2 LS-DYNA Student 12.0.0\\LS-DYNA\\env.ps1"
        self.lspp_powershell_env_dir_path = os.path.dirname(self.lspp_powershell_env_path)
        self.current_path = "C:\\Users\\CsungaBro\\Documents\\code\\dl-simulation\\ls-dyna-automatization"
        self.lspp_env_command = "Set-Alias lspp $ENV:ANSYS_STUDENT_LSDYNA_LSPREPOST_PATH"
        self.lsrun_env_command = "Set-Alias lsrun $ENV:ANSYS_STUDENT_LSDYNA_LSRUN_PATH"
        self.k_file_path_container = []
        self.lsrun_first_in = False

    def lspp_powershell_maker(self, c_file_path):
        path_of_lspp_powershell = "powershell_scripts\\lspp_powershell.ps1"
        with open(path_of_lspp_powershell, "w") as fsp:
            fsp.write(r'cd "{}"'.format(self.lspp_powershell_env_dir_path))
            fsp.write("\n")
            fsp.write(r'{}'.format(self.lspp_env_command))
            fsp.write("\n")
            fsp.write(r'cd "{}"'.format(self.current_path))
            fsp.write("\n")
            fsp.write(r'lspp c={} -nographics'.format(c_file_path))
        return path_of_lspp_powershell

    def lsrun_powershell_maker(self, k_file_path):
        self.path_of_lsrun_powershell = "powershell_scripts\\lsrun_powershell.ps1"
        k_file_full_path = os.path.abspath(k_file_path)
        mode = "w" if not self.lsrun_first_in else "a"
        with open(self.path_of_lsrun_powershell, mode) as fsp:
            if not self.lsrun_first_in:
                fsp.write(r'cd "{}"'.format(self.lspp_powershell_env_dir_path))
                fsp.write("\n")
                fsp.write(r'{}'.format(self.lsrun_env_command))
                fsp.write("\n")
                fsp.write(r'cd "{}"'.format(self.current_path))
                fsp.write("\n")
                fsp.write(r'lsrun {} -submit -cleanjobs'.format(k_file_full_path))
                fsp.write("\n")
                fsp.write("Start-Sleep 1")
                self.lsrun_first_in = True
            else:
                fsp.write("\n")
                fsp.write(r'lsrun {} -submit -wait -1'.format(k_file_full_path))
                fsp.write("\n")
                fsp.write("Start-Sleep 1")

    def lsdyna_command_runner(self, c_file_path, k_file_path):
        path_of_lspp_powershell = self.lspp_powershell_maker(c_file_path)
        self.lsrun_powershell_maker(k_file_path)
        completed1 = subprocess.run(["powershell", ".\{}".format(path_of_lspp_powershell)], capture_output=True)
        # completed1 = subprocess.run(["powershell", ".\{}".format(path_of_lsrun_powershell)], capture_output=True)
        self.k_file_path_container.append(k_file_path)

    def lsrun_command_runner(self):
        completed1 = subprocess.Popen(["powershell", ".\{}".format(self.path_of_lsrun_powershell)])
        print(completed1)



class ScriptRunner:
    def __init__(self, number_of_files, FileHandler, PowershellRunner, FileManipulator ):
        self.number_of_files = number_of_files
        self.FileHandler = FileHandler
        self.PowershellRunner = PowershellRunner
        self.FileManipulator = FileManipulator
    
    def k_file_generator(self):
        for files in range(self.number_of_files):
            paths = self.FileHandler.files_preper()
            c_file_path, k_file_path = paths[0], paths[1]
            self.FileManipulator.c_file_save_adder(c_file_path, k_file_path)
            self.PowershellRunner.lsdyna_command_runner(c_file_path, k_file_path)
        self.PowershellRunner.lsrun_command_runner()


if __name__ == "__main__":
    c_files_path = "output\\c_files"
    k_files_path = "output\\k_files"
    FH = FileHandler(c_files_path, k_files_path)
    FM = FileManipulator("template\\save_temp.cfile")
    PR = PowershellRunner()
    SC = ScriptRunner(FH.c_files_to_prep, FH, PR, FM)
    SC.k_file_generator()