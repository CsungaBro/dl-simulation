import os
from re import search 
import regex as re

class FileHandler:
    def __init__(self, k_file_folder_path, png_maker_path):
        self.k_file_folder_path =  k_file_folder_path
        self.png_maker_path = png_maker_path
        self.k_file_folders = self.folder_lister()

    def folder_lister(self):
        return os.listdir(self.k_file_folder_path)


class CFileManipulator:
    def __init__(self, png_maker_path):
        self.png_maker_path = png_maker_path

    def c_file_manipulation(self, k_file_folder_path):
        self.new_c_file_name = "{}_png_gen.cfile".format(os.path.dirname(k_file_folder_path))
        self.new_c_file_path = os.path.join(k_file_folder_path, self.new_c_file_name)
        self.new_png_path = re.sub("cfile", "png", self.new_c_file_path)
        self.output_path = os.join(k_file_folder_path, "d3plot")
        with open(self.png_maker_path, "r") as fr, open(self.new_c_file_path, "w") as fw:
            for line in fr:
                fw.writelines(self.process(line))
    
    def process(self, line):
        search_1 = "open d3plot"
        search_2 = "print png"
        new_line_1 = 'open d3plot "{}"'.format(self.output_path)
        new_line_2 = 'print png "{}" enlisted "OGL1x1" '.format(self.new_png_path)
        if bool(search_1, line):
            return new_line_1
        if bool(search_2, line):
            return new_line_2
        return line


if __name__ == "__main__":
    FH = FileHandler()