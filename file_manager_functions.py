import os
import io
import PySimpleGUI as sg
import shutil

new_destination=None
copied_files:str=[]
def choose_folder():
    sg.FolderBrowse()

def move(values):
    print("test")
    copy(values)
    # delete(values)
    #move is just copy and delete. so probably just do that. 

def rename(values):
    new_name = sg.popup_get_text("Enter new name:", default_text=os.path.basename(values))
    if new_name:
        os.rename(values, os.path.join(os.path.dirname(values), new_name))

def sort():
    return None

def delete(values):
    #needs the file location 
    for f in values:
        os.remove(f)
    sg.popup(f"{values} successfully deleted")


def copy(values):
    copied_files=[]
    try:
        for file in values:
            print(file)
            copied_files.append(file)
    except IOError as e: 
        print(f"Error copying file:{e}")

"""
values (str list): this list contains the files to pasted
new_destination (str): this string contains the destination where the files are to be
placed.
"""

def paste(new_destination):
    #only show up if move or copy is called
    # from looking at the file manager, they still show up the paste value, but the paste option
    # is disabled. 
    #need to do the new destination thing
    # i guess for now, do something "for file in values, shutil copy into new destination?"
    
    try:
        for file in copied_files:
            shutil.copy(file,new_destination)
        copied_files=[]
    except IOError as e:
        print(f"Error copying file: {e}")
    return None
