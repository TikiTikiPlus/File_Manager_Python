#do something with the ui to pop up
# img_viewer.py

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

imgdata=None
file_chosen: bool
name_of_file: str
tags: list
tags=[]
# First the window layout in 2 columns
file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]
tags_column = [
    [sg.Text("Tag image chosen"),
     sg.In(size=(40, 1),
    enable_events=True, key="-TAGS-"),
    sg.B('Tag')],
    [
        sg.Listbox(
            values=tags, enable_events=True, size=(40,20), key="-TAG LIST-"
        )
    ]
]
image_viewer_column = [

    [sg.Text("Choose an image from list on left:")],

    [sg.Text(size=(40, 1), key="-TOUT-")],

    [sg.Image(key="-IMAGE-", data=imgdata)],

]
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(tags_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout)
db=sqlite3.connect("./image_database.db", uri=True)

cursor=db.cursor()
file_chosen=False
last_clicked_item = None
current_clicked_item=None
while True:

    event, values = window.read()
    if event == "-FOLDER-":

        folder = values["-FOLDER-"]

        try:

            # Get list of files in folder
            file_list = os.listdir(folder)

        except:

            file_list = []


        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif",".jpg"))
        ]

        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox

        try:

            filename = os.path.join(

                values["-FOLDER-"], values["-FILE LIST-"][0]

            )
            
            
            window["-TOUT-"].update(filename)

            # image = Image.open(filename)
            # imgdata = image.tobytes()
            window["-IMAGE-"].update(filename=filename)
            #list out the tags of the of the image
            file_chosen=True
            name_of_file=hashlib.md5(open(filename,'rb').read()).hexdigest()
            #if there is none, show none



        except:

            pass
    elif event == 'Tag':
        #check if the photo is in the database. 
        #we can try the md5sum 
        #check what happens first
        #print the name of the file
        
        #check if file exists in the local database

        # create_table_query = '''
        # CREATE TABLE IF NOT EXISTS images (
        #     image_name TEXT PRIMARY KEY,
        #     tags TEXT
        # );
        # '''

        # # Execute the SQL statement to create the table
        # cursor.execute(create_table_query)

        # # Commit the changes and close the connection
        # db.commit()
        # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        # # Fetch all the table names
        # tables = cursor.fetchall()
        # print(tables)
        cursor.execute("SELECT * FROM images WHERE image_name=?",(name_of_file,))
        image_name = cursor.fetchone()
        tag=values['-TAGS-']
        if image_name is None:
            print("Image does not exist yet")
            #insert the image name into the database
            tag=[tag]

            cursor.execute("INSERT INTO images (image_name, tags) VALUES (?,?);", (name_of_file,str(tag)))
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
    elif event=="-TAG LIST-":
        #if something is clicked twice within a certain amount of time, the user will be prompt if they want the tag to be removed.
        last_clicked_item=current_clicked_item
        current_clicked_item = values['-TAG LIST-'][0]
        if current_clicked_item == last_clicked_item:
            confirm_popup = sg.popup_yes_no("Remove this tag?")
            if confirm_popup=='Yes':
                sql_query = "SELECT tags FROM images where image_name=?;"
                cursor.execute(sql_query, (name_of_file,))
                tags=cursor.fetchall()
                tags=tags[0][0]
                tags=ast.literal_eval(tags)
                updated_tags = [item for item in tags if current_clicked_item!=item]
                print(len(updated_tags))
                if len(updated_tags)<1:
                    #remove the entry in the database
                    delete_entry="DELETE from images where image_name=?;"
                    cursor.execute(delete_entry,(name_of_file,))
                else:

                #insert the new tags into the image. 
                    update_array_query = "UPDATE images SET tags = ? WHERE image_name = ?;"
                    cursor.execute(update_array_query, (str(updated_tags), name_of_file))
                db.commit()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    #I want the tag to always be updated no matter what is pressed. therefore i'd have to place the function here. 
    if file_chosen:
        try:
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
        except: 
            continue


#once the ui pops up, check the files in root. 

#then, can maybe expand from there? once that is done, we can possibly do tagging

#some with existing, and creating new tag option