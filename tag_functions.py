
from cgi import test
import PySimpleGUI as sg
import os.path
from PIL import Image
import io
import base64
import hashlib
import sqlite3
from urllib.request import pathname2url
import ast
import imghdr
from search_functions import *
from file_checks import check_image_with_pil
import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk

def resize_image(image_path, target_size):
    original_image = Image.open(image_path)
    resized_image = original_image.resize(target_size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(resized_image)

file_chosen=False
last_clicked_item = None
current_clicked_item=None

def get_file_list(folder_path):
    #Gets file of list in the folder
    try:
        file_list = os.listdir(folder_path)
        return file_list
    except OSError as e:
        sg.popup_error(f"Error reading folder: {e}")
        return []

# while True:
def open_folder(window, values):
#     event, values = window.read()
    # if event == "-FOLDER-":

    folder = values["-FOLDER-"]
    try:

        # Get list of files in folder
        file_list = os.listdir(folder)

    except:

        file_list = []
    window["-FILE LIST-"].update(file_list)
    return folder
# elif event == "-FILE LIST-":  # A file was chosen from the listbox
def file_list(window, folder, filename):
    try:
        # partial_filename=values["-FILE LIST-"][0]
        # print(partial_filename)
        full_filename = os.path.join(
            folder,filename
        )
        window["-TOUT-"].update(full_filename)
        # image = Image.open(filename)
        # imgdata = image.tobytes()
        # if imghdr.write(path):
        if check_image_with_pil(full_filename):
            # pil_image = Image.open(full_filename)
            # img_bytes = convert_image_to_bytes(pil_image)
            resized_image = resize_image(full_filename,(300,300))
            window["-IMAGE-"].update(data=resized_image)
        else:
            window["-IMAGE-"].update(data=None)
        
        #list out the tags of the of the image
        file_chosen=True
        hashed_filename=hashlib.md5(open(full_filename,'rb').read()).hexdigest()
        #if there is none, show none
        return hashed_filename, full_filename, file_chosen
    except:
        pass

# elif event == 'Tag':
def tag(db, cursor, name_of_file, filename, values):
    cursor.execute("SELECT * FROM images WHERE image_name=?",(name_of_file,))
    image_name = cursor.fetchone()
    tag=values['-TAGS-']
    tag=tag.replace(" ","_")
    
    if image_name is None:
        print("Image does not exist yet")
        #insert the image name into the database
        tag=[tag]
        filename=[filename]
        cursor.execute("INSERT INTO images (image_name, tags, location) VALUES (?,?,?);", (name_of_file,str(tag),str(filename).replace("\\\\",'\\')))
        db.commit()
    else:
        cursor.execute("SELECT * FROM images WHERE image_name=?;",(name_of_file,))
        tags=cursor.fetchone()
        array_text=tags[1]
        array_list = ast.literal_eval(array_text)
        if tag in array_list:
            print("This image is already tagged with the same tags")
        else:
            array_list.append(tag)
            update_array_query = "UPDATE images SET tags = ? WHERE image_name = ?;"
            cursor.execute(update_array_query, (str(array_list), name_of_file))
        # Commit the changes
            db.commit()
        #get the tags into

# elif event=="-TAG LIST-":
def tag_list(cursor, values, db, name_of_file):
    #if something is clicked twice within a certain amount of time, the user will be prompt if they want the tag to be removed.
    
    try:
            confirm_popup = sg.popup_yes_no("Remove this tag?")
            if confirm_popup=='Yes':
                sql_query = "SELECT tags FROM images where image_name=?;"
                cursor.execute(sql_query, (name_of_file,))
                tags=cursor.fetchall()
                tags=tags[0][0]
                tags=ast.literal_eval(tags)
                updated_tags = [item for item in tags if values!=item]
                if len(updated_tags)<1:
                    #remove the entry in the database
                    delete_entry="DELETE from images where image_name=?;"
                    cursor.execute(delete_entry,(name_of_file,))
                else:

                #insert the new tags into the image. 
                    update_array_query = "UPDATE images SET tags = ? WHERE image_name = ?;"
                    cursor.execute(update_array_query, (str(updated_tags), name_of_file))
                db.commit()
    except Exception as e:
        print(e)
#I want the tag to always be updated no matter what is pressed. therefore i'd have to place the function here. 
# if file_chosen:
def tag_check(cursor,name_of_file, window):
    cursor.execute("SELECT tags FROM images WHERE image_name=?",(name_of_file,))
    tags = cursor.fetchone()
    #array_text=tags[0]
    window['-TAG LIST-'].update(disabled=False)
    if tags is None:
        tags=[]
        array_list=['There are currently no tags on this image']
        for tag in array_list:
            tags.append(tag)
        window["-TAG LIST-"].update(tags)
        window['-TAG LIST-'].update(disabled=True)
    #disable clicking on the tag listbox
    else: 
        array_list = ast.literal_eval(tags[0])
        tags=[]
        for tag in array_list:
            tags.append(tag)
        window["-TAG LIST-"].update(tags)