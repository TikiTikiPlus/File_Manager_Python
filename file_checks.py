import sqlite3
import os
import hashlib
import imghdr
import filetype
format = [".jpg",".png",".jpeg"]
# Connect to the database (change the database name and table/column names accordingly)
def list_files(folder_path):
    files_and_folder = os.listdir(folder_path)
    # this lists all the files and folders. and can also differentiate from files and folders
    # when we do use it. 
    files = [file for file in files_and_folder if os.path.isfile(os.path.join(folder_path, file))]
    folders = [folder for folder in files_and_folder if os.path.isdir(os.path.join(os.path.join(folder_path, folder)))]
    return files, folders

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
                        # drive_letter = os.path.splitdrive(abs_path)[0]
                        # print(abs_path)
                        # print(file_path)
                        # print("file_found")
                        return abs_path

    return None
