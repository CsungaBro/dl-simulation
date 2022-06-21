import tensorflow as tf
import matplotlib.pyplot as plt
from logger.csu_logger import logger_init
import os
import shutil
import regex as re
from PIL import Image 

class DataRenamer:
    def __init__(self, x_data_path, y_data_path, folder_handler) -> None:
        self.x_data_path = x_data_path
        self.y_data_path = y_data_path
        self.new_x = folder_handler.loc_x_folder_raw
        self.new_y = folder_handler.loc_y_folder_raw

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
    def __init__(self, loc_x_folder_raw, loc_y_folder_raw, loc_x_folder_clean, loc_y_folder_clean ) -> None:
        self.loc_x_folder_raw = loc_x_folder_raw
        self.loc_x_folder_clean = loc_x_folder_clean
        self.loc_y_folder_raw = loc_y_folder_raw
        self.loc_y_folder_clean = loc_y_folder_clean 
    
    def make_folders(self):
        for folder in [self.loc_x_folder_raw, self.loc_x_folder_clean, self.loc_y_folder_raw, self.loc_y_folder_clean]:
            if not os.path.exists(folder):
                os.mkdir(folder)

    def file_list(self, folder_name):
        return os.listdir(folder_name)


class ImageManipulation:
    def __init__(self, folder_handler) -> None:
        self.folder_handler = folder_handler
        self.crop_parameter_init()

    def crop_parameter_init(self):
        self.x_data_crop_param = {
            'x_1': 240,
            'y_1':112,
            'x_2': 783,
            'y_2':655,            
        }
        self.y_data_crop_param = {
            'x_1': 465,
            'y_1':1,
            'x_2': 1170,
            'y_2':705,            
        }

    def crop_image(self, image_path, crop_param):
        im = Image.open(image_path)
        return im.crop((crop_param["x_1"], crop_param["y_1"], crop_param["x_2"], crop_param["y_2"]))        

    def image_processor(self, image_path, clean_path, crop_param):
        img_crp = self.crop_image(image_path, crop_param)
        image_name = os.path.basename(image_path)
        img_crp.save(os.path.join(clean_path, image_name))
        
    def data_processor(self, raw_path, clean_path, crop_param):
        for image_name in self.folder_handler.file_list(raw_path):
            self.image_processor(os.path.join(raw_path, image_name), clean_path, crop_param)
    
    def main(self):
        self.data_processor(self.folder_handler.loc_x_folder_raw, self.folder_handler.loc_x_folder_clean, self.x_data_crop_param)
        self.data_processor(self.folder_handler.loc_y_folder_raw, self.folder_handler.loc_y_folder_clean, self.y_data_crop_param)


def main(x_data_path, y_data_path, loc_x_folder_raw, loc_y_folder_raw, loc_x_folder_clean, loc_y_folder_clean):
    logger.info(f"TensorFlow version:{tf.__version__}")
    folder_handler = FolderHandler(loc_x_folder_raw, loc_y_folder_raw, loc_x_folder_clean, loc_y_folder_clean)
    folder_handler.make_folders()
    data_renamer = DataRenamer(x_data_path, y_data_path, folder_handler)
    data_renamer.copy_datas()
    image_manipulator = ImageManipulation(folder_handler)
    image_manipulator.main()
    

if __name__ =="__main__":
    logger = logger_init()
    curv_data_path = "C:\\Users\\CsungaBro\\Documents\\code\\dl-simulation\\ls-dyna-automatization\\output\\curv"
    sim_data_path = "C:\\Users\\CsungaBro\\Documents\\code\\dl-simulation\\ls-dyna-automatization\\output\\sim"
    loc_x_folder_raw = "raw\\x-data"
    loc_x_folder_clean = "clean\\x-data"
    loc_y_folder_raw = "raw\\y-data"
    loc_y_folder_clean = "clean\\y-data"
    main(curv_data_path, sim_data_path, loc_x_folder_raw, loc_y_folder_raw, loc_x_folder_clean, loc_y_folder_clean)