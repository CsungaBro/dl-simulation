import os
import shutil


class FileHandler:
    def __init__(self, k_folder_path, c_folder_path, output_path) -> None:
        self.k_folder_path = k_folder_path
        self.c_folder_path = c_folder_path
        self.output_path = output_path
    
    def file_zipper(self):
        self.folder_creator(self.output_path)
        self.folder_copy([self.k_folder_path, self.c_folder_path], self.output_path)
        output_name = os.path.basename(self.output_path)
        output_dir = os.path.dirname(self.output_path)
        shutil.make_archive(os.path.join(output_dir, output_name), 'zip', self.output_path)

    def folder_creator(self, folder_path):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    def folder_copy(self, srcs, dst):
        for src in srcs:
            dir_name = os.path.basename(src)
            shutil.copytree(src, os.path.join(dst, dir_name))


if __name__ == "__main__":
    k_folder_path = 'output\\k_files'
    c_folder_path = 'output\\c_files'
    output_path = 'export\\all_inp_04'
    file_handler = FileHandler(k_folder_path, c_folder_path, output_path)
    file_handler.file_zipper()