import os 
from PIL import Image

def image_resize(image_in_path, image_out_path, IMG_SIZE):
    img = Image.open(image_in_path)
    img_rs = img.resize(IMG_SIZE)
    img_rs.save(image_out_path)

def image_handler(data_path, data_rs_path, IMG_SIZE):
    file_names = os.listdir(data_path)
    file_number = len(file_names)
    for count, file_name in enumerate(file_names):
        image_in_path = os.path.join(data_path, file_name)
        image_out_path = os.path.join(data_rs_path, file_name)
        image_resize(image_in_path, image_out_path, IMG_SIZE)
        print(f"{count+1} / {file_number}")

def main(x_data, y_data, x_data_rs, y_data_rs, IMG_SIZE):
    image_handler(x_data, x_data_rs, IMG_SIZE)
    image_handler(y_data, y_data_rs, IMG_SIZE)

if __name__ == '__main__':
    IMG_SIZE = (256,256)
    x_data = 'clean\\x-data'
    y_data = 'clean\\y-data'
    x_data_rs = 'clean\\x-data-rs'
    y_data_rs = 'clean\\y-data-rs'
    main(x_data, y_data, x_data_rs, y_data_rs, IMG_SIZE)