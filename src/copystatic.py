import os
import shutil

def copy_files_recursively(src, dst):
    if os.path.exists(src):
        dirs = os.listdir(src)
        for dir in dirs:
            dir_path = os.path.join(src, dir)
            if os.path.isfile(dir_path):
                new_copy = shutil.copy(dir_path, dst)
                print(f"new copy -> {new_copy}")
            else:
                new_dir = os.path.join(dst, dir)
                os.mkdir(new_dir)
                copy_files_recursively(dir_path, new_dir)
