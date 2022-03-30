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
    def __init__(self):
        self.save_part = "template\\save_temp.cfile"

    def c_file_manipulator(self, c_file, k_file):
        with open(c_file,"a") as fr, open(self.save_part, "r") as fs:
            for line in fs:
                if bool(re.search("path", line)):
                    k_file_full_path = os.path.abspath(k_file)
                    new_line = r'save keyword "{}"'.format(k_file_full_path)
                    fr.writelines(new_line)
                else:
                    fr.writelines(line)


class PowershellRunner:
    def __init__(self, FileManipulator):
        self.lspp_powershell_env_path = "D:\\Program Files\\ANSYS 2020R2 LS-DYNA Student 12.0.0\\LS-DYNA\\env.ps1"
        self.lspp_powershell_env_dir_path = os.path.dirname(self.lspp_powershell_env_path)
        self.current_path = "C:\\Users\\CsungaBro\\Documents\\code\\dl-simulation\\ls-dyna-automatization"
        self.lspp_env_command = "Set-Alias lspp $ENV:ANSYS_STUDENT_LSDYNA_LSPREPOST_PATH"
        self.lsrun_env_command = "Set-Alias lsrun $ENV:ANSYS_STUDENT_LSDYNA_LSRUN_PATH"
        self.FileManipulator = FileManipulator
        self.k_file_path_container = []
        self.lsrun_first_in = False

    def lspp_powershell_maker(self, c_file_path):
        path_of_lspp_powershell = "lspp_powershell.ps1"
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
        path_of_lsrun_powershell = "lsrun_powershell.ps1"
        k_file_full_path = os.path.abspath(k_file_path)
        with open(path_of_lsrun_powershell, "w") as fsp:
            fsp.write(r'cd "{}"'.format(self.lspp_powershell_env_dir_path))
            fsp.write("\n")
            fsp.write(r'{}'.format(self.lsrun_env_command))
            fsp.write("\n")
            fsp.write(r'cd "{}"'.format(self.current_path))
            fsp.write("\n")
            if not self.lsrun_first_in:
                fsp.write(r'lsrun {} -submit -cleanjobs'.format(k_file_full_path))
                self.lsrun_first_in = True
            else:
                fsp.write(r'lsrun {} -submit -wait -1'.format(k_file_full_path))
        return path_of_lsrun_powershell

    def lspp_command_runner(self, paths):
        c_file_path, k_file_path = paths[0], paths[1]
        self.FileManipulator.c_file_manipulator(c_file_path, k_file_path)
        path_of_lspp_powershell = self.lspp_powershell_maker(c_file_path)
        path_of_lsrun_powershell = self.lsrun_powershell_maker(k_file_path)
        #completed1 = subprocess.run(["powershell", ".\{}".format(path_of_lspp_powershell)], capture_output=True)
        completed1 = subprocess.run(["powershell", ".\{}".format(path_of_lsrun_powershell)], capture_output=True)
        print(completed1)
        self.k_file_path_container.append(k_file_path)



    def fafo(self, c_file_path: str):
        print("FAFO")
        print(c_file_path)
        env = {"PATH": self.lspp_powershell_env_path}
        command_1 = 'cd "D:/Program Files/ANSYS 2020R2 LS-DYNA Student 12.0.0/LS-DYNA"\n'
        command_2 = "Set-Alias lspp $ENV:ANSYS_STUDENT_LSDYNA_LSPREPOST_PATH\n"
        command_3 = 'cd "C:/Users/CsungaBro/Google Drive/TU Braunschweig/3. Semester/COURSE 0 - Studienarbeit/33-dl-sim/dl-simulation/ls-dyna-automatization"\n'
        command_4 = "lspp c={} -nographics".format(c_file_path)
        commands = [command_1, command_2, command_3, command_4]
        psc_2 = "test_2.ps1"
        with open(psc_2, "w") as f:
            for command in commands:
                f.write("{}".format(command))
        psc_1 = "test.ps1"
        # print(commands)
        completed1 = subprocess.run(["powershell", ".\{}".format(psc_2)], capture_output=True)
        # completed1 = subprocess.run(["powershell", command_1], capture_output=True)
        # completed2 = subprocess.run(["powershell", command_2], capture_output=True)
        # completed3 = subprocess.run(["powershell", command_3], capture_output=True)
        # completed4 = subprocess.run(["powershell", command_4], capture_output=True)

        # completed = subprocess.run(["powershell", "-Command", command_1, command_2, command_3, command_4], capture_output=True)
        print(completed1)
    def fafo2(self, k_file_path: str):
        command_1 = 'cd "D:/Program Files/ANSYS 2020R2 LS-DYNA Student 12.0.0/LS-DYNA"\n'
        command_2 = "Set-Alias lsrun $ENV:ANSYS_STUDENT_LSDYNA_LSRUN_PATH\n"
        command_3 = 'cd "C:/Users/CsungaBro/Google Drive/TU Braunschweig/3. Semester/COURSE 0 - Studienarbeit/33-dl-sim/dl-simulation/ls-dyna-automatization/output/k_files/01"\n'
        command_4 = "lsrun i={}".format(k_file_path)        
        # command_4 = "lsrun i={} ncpu=4 memory=20m".format(k_file_path)        
        commands = [command_1, command_2, command_3, command_4]
        psc_3 = "test_3.ps1"
        with open(psc_3, "w") as f:
            for command in commands:
                f.write("{}".format(command))
        psc_1 = "test.ps1"
        # print(commands)
        completed1 = subprocess.run(["powershell", ".\{}".format(psc_3)], capture_output=True)

class ScriptRunner:
    def __init__(self, number_of_files, FileHandler, PowershellRunner ):
        self.number_of_files = number_of_files
        self.FileHandler = FileHandler
        self.PowershellRunner = PowershellRunner
    
    def k_file_generator(self):
        for files in range(self.number_of_files):
            self.PowershellRunner.lspp_command_runner(self.FileHandler.files_preper())


if __name__ == "__main__":
    c_files_path = "output\\c_files"
    k_files_path = "output\\k_files"
    FH = FileHandler(c_files_path, k_files_path)
    FM = FileManipulator()
    PR = PowershellRunner(FM)
    SC = ScriptRunner(FH.c_files_to_prep, FH, PR)
    SC.k_file_generator()
    
    # PR.fafo("output\\c_files\\test.cfile")
    # PR.fafo2("C:\\Users\\CsungaBro\\Google Drive\\TU Braunschweig\\3. Semester\\COURSE 0 - Studienarbeit\\33-dl-sim\\dl-simulation\\ls-dyna-automatization\\output\\k_files\\01\\plsss.k")