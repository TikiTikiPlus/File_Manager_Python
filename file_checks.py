import sqlite3
import os
import hashlib
import imghdr
import filetype
import PIL
import time
format = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
# Connect to the database (change the database name and table/column names accordingly)
# def list_files(folder_path):
#     files_and_folder = os.listdir(folder_path)
#     # this lists all the files and folders. and can also differentiate from files and folders
#     # when we do use it. 
#     files = [file for file in files_and_folder if os.path.isfile(os.path.join(folder_path, file))]
#     folders = [folder for folder in files_and_folder if os.path.isdir(os.path.join(os.path.join(folder_path, folder)))]
#     return files, folders

DOUBLE_CLICK_TIME_THRESHOLD=3.0
last_clicked_time:int=None
last_clicked_item:str = None
def handle_double_click(values):
    global last_clicked_time
    global last_clicked_item

    current_time=time.time()
    if last_clicked_time is not None:

        time_difference= current_time - last_clicked_time
        if time_difference < DOUBLE_CLICK_TIME_THRESHOLD and last_clicked_item == values:
            return True
    last_clicked_item=values
    last_clicked_time = current_time
    return False
def check_image_with_pil(path):
    try:
        PIL.Image.open(path)
    except IOError:
        return False
    return True
#check if the path is a folder or file
def identify_path(path):
    #chekck if path is a file
    if os.path.isdir(path):
        return "Folder"
    elif os.path.isfile(path):
        return "File"
    else:
        return "Not Found"

def calculate_file_hash(file_path):
    try:
    #"""Calculate the hash of a file."""
        hashed_filename=hashlib.md5(open(file_path,'rb').read()).hexdigest()
        return hashed_filename
    except PermissionError:
        print(f"Permission denied for file: {file_path}")

def find_file_by_hash(target_hash, search_directory="/"):
    #"""Find a file by comparing its hash with a target hash."""
    for root, dirs, files in os.walk(search_directory):
        
        for filename in files:
                
                file_path = os.path.join(root, filename)
                if file_path.endswith(tuple(format)):
                    hashed = calculate_file_hash(file_path=file_path)
                    if hashed == target_hash:
                        abs_path = os.path.abspath(file_path)
                        return abs_path

    return None
