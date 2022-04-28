import os
import shutil

class FileCopy:
    def file_copy(self, src_path, dest_dir):
        scr_name = os.path.basename(src_path)
        dest_path = os.path.join(dest_dir, scr_name)
        shutil.copyfile(src_path, dest_path)
