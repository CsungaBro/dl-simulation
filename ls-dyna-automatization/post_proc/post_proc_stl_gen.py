import os
from re import search 
import regex as re

class CFileSTLManipulator:
    def __init__(self, stl_maker_path):
        self.stl_maker_path = stl_maker_path
        self.actual_path = 1

    def c_file_manipulation(self, k_file_folder_path):
        self.new_c_file_name = "{}_stl_gen.cfile".format(os.path.basename(k_file_folder_path))
        self.new_c_file_path = os.path.join(k_file_folder_path, self.new_c_file_name)
        self.new_png_path = re.sub(".cfile", "", self.new_c_file_path)
        self.output_path = os.path.join(k_file_folder_path, "d3plot")
        print(self.new_c_file_path)
        with open(self.stl_maker_path, "r") as fr, open(self.new_c_file_path, "w") as fw:
            for line in fr:
                fw.writelines(self.process(line))
        self.actual_path = 1                
    
    def process(self, line):
        search_1 = "open d3plot"
        search_2 = "output"
        new_line_1 = 'open d3plot "{}"\n'.format(self.output_path)
        # new_line_2 = 'print png "{}" enlisted "OGL1x1" '.format()
        new_line_2 = f'output "{self.new_png_path}{self.actual_path}_25.stl" 1 8 0 0\n'
        if bool(re.search(search_1, line)):
            return new_line_1
        if bool(re.search(search_2, line)):
            self.actual_path += 1  
            return new_line_2
        return line