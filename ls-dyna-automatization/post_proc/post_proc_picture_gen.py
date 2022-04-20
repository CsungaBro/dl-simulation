import os
from re import search 
import regex as re
import ls_c_runner as ls

class FileHandler:
    def __init__(self, k_folder_path, png_maker_path):
        self.k_folder_path =  k_folder_path
        self.png_maker_path = png_maker_path
        self.k_file_folders = self.folder_lister()
        [print(x) for x in self.k_file_folders]

    def folder_lister(self):
        return [os.path.join(self.k_folder_path, folder) for folder in os.listdir(self.k_folder_path)]


class CFileManipulator:
    def __init__(self, png_maker_path):
        self.png_maker_path = png_maker_path

    def c_file_manipulation(self, k_file_folder_path):
        self.new_c_file_name = "{}_png_gen.cfile".format(os.path.basename(k_file_folder_path))
        self.new_c_file_path = os.path.join(k_file_folder_path, self.new_c_file_name)
        self.new_png_path = re.sub("cfile", "png", self.new_c_file_path)
        self.output_path = os.path.join(k_file_folder_path, "d3plot")
        print(self.new_c_file_path)
        with open(self.png_maker_path, "r") as fr, open(self.new_c_file_path, "w") as fw:
            for line in fr:
                fw.writelines(self.process(line))
    
    def process(self, line):
        search_1 = "open d3plot"
        search_2 = "print png"
        new_line_1 = 'open d3plot "{}"'.format(self.output_path)
        new_line_2 = 'print png "{}" enlisted "OGL1x1" '.format(self.new_png_path)
        if bool(re.search(search_1, line)):
            return new_line_1
        if bool(re.search(search_2, line)):
            return new_line_2
        return line


if __name__ == "__main__":
    k_dir_path = "output\\k_files"
    c_file_template_path = "template\image_gen.cfile"

    FH = FileHandler(k_dir_path, c_file_template_path)
    CFM = CFileManipulator(c_file_template_path)
    KFG = ls.KFileGenerator()
    for folder in FH.k_file_folders:
        CFM.c_file_manipulation(folder)
        KFG.lsrun_command_runner(CFM.new_c_file_path)