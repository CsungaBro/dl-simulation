import tensorflow as tf
import matplotlib.pyplot as plt
from logger.csu_logger import logger_init
import os
import shutil
import regex as re

class DataRenamer:
    def __init__(self, x_data_path, y_data_path, folder_handler) -> None:
        self.x_data_path = x_data_path
        self.y_data_path = y_data_path
        self.new_x = folder_handler.loc_x_folder
        self.new_y = folder_handler.loc_y_folder

    def copy_datas(self):
        self.copy_data(self.x_data_path, self.new_x)
        self.copy_data(self.y_data_path, self.new_y)

    def copy_data(self, data_path, new_path) -> None:
        files = os.listdir(data_path)
        for file in files:
            new_file = self.rename_file(file)
            old_file_path = os.path.join(data_path, file)
            new_file_path = os.path.join(new_path, new_file)
            shutil.copy(old_file_path, new_file_path)

    def rename_file(self, file_name):
        sim_name = re.findall("sim_[0-9]+", file_name)[0]
        data_id = re.sub("sim_", "", sim_name)
        id_name = f"{data_id}.png"
        logger.info(id_name)
        return id_name


class FolderHandler:
    def __init__(self, loc_x_folder, loc_y_folder) -> None:
        self.loc_x_folder = loc_x_folder
        self.loc_y_folder = loc_y_folder
    
    def make_folders(self):
        if not os.path.exists(self.loc_x_folder):
            os.mkdir(self.loc_x_folder)
        if not os.path.exists(self.loc_y_folder):
            os.mkdir(self.loc_y_folder)            


def main(x_data_path, y_data_path, loc_x_folder, loc_y_folder):
    logger.info(f"TensorFlow version:{tf.__version__}")
    folder_handler = FolderHandler(loc_x_folder, loc_y_folder)
    folder_handler.make_folders()
    data_renamer = DataRenamer(x_data_path, y_data_path, folder_handler)
    data_renamer.copy_datas()
    

if __name__ =="__main__":
    logger = logger_init()
    curv_data_path = "C:\\Users\\CsungaBro\\Documents\\code\\dl-simulation\\ls-dyna-automatization\\output\\curv"
    sim_data_path = "C:\\Users\\CsungaBro\\Documents\\code\\dl-simulation\\ls-dyna-automatization\\output\\sim"
    loc_x_folder = "x-data"
    loc_y_folder = "y-data"
    main(curv_data_path, sim_data_path, loc_x_folder, loc_y_folder)