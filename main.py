import PySimpleGUI as sg
from tag_layout import tagging_layout
from search_layout import search_layout
import sqlite3
from search_functions import *
from tag_functions import *
from file_checks import *
import tkinter as tk
from file_manager_functions import *

hashed_filename: str
filename: str
file_chosen=False
new_destination:str=None
# Create the TabGroup with tabs
layout = [
    [sg.TabGroup([
        [sg.Tab('Tag Images', tagging_layout)],
        [sg.Tab('Search Images', search_layout)],
        # [sg.Tab('Tab 3', tab3_layout)]
    ])],
    [sg.Button('Exit')]
]
window = sg.Window('Tabbed Interface', layout)
db=sqlite3.connect("./tags_database.db", uri=True)

cursor=db.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='images'")

result=cursor.fetchone()

if not result:

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS images (
        image_name TEXT PRIMARY KEY,
        tags TEXT,
        location TEXT
    );
    '''

    # Execute the SQL statement to create the table
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    db.commit()

cursor.execute("SELECT * FROM images")    

hashed_filename=""
current_path="C:/"
while True:

    event, values = window.read()
    # search functions
    if event == "Search":
        search(values=values, db = db, window=window)
    elif event =="-IMAGE LIST-":
        search_image_list(window=window, values = values)
    elif event=="-FOLDER-":
        current_path=open_folder(window=window, values=values)
    elif event == "-FILE LIST-":
        element=window.find_element_with_focus()       
        path=values["-FILE LIST-"][0]
        full_path=os.path.join(current_path,path)
        if handle_double_click(path):
            file_type=identify_path(full_path)
            if file_type=="File":
            #check if chosen file is folder. if chosen file is folder, then 
            #proceed and redo the get_file_list thing.
                hashed_filename, filename, file_chosen=file_list(window=window,folder=current_path, filename=path)
            elif file_type=="Folder":
                #do a separate one. where if the folder is chosen, it would show a new 
                #set of files
                window["-FILE LIST-"].update(get_file_list(full_path))
                current_path=full_path
                window["-FOLDER-"].update(full_path)
    elif event=='Move':
        files:str=[]
        #maybe something like appending the file paths
        # file_path = values["-FOLDER-"]
        for i,f in enumerate(values["-FILE LIST-"]):
            absolute_file=os.path.join(current_path, f)
            print(absolute_file)
            files.append(absolute_file)
        
        move(files)
    elif event =='Rename':
        rename(values)
    elif event == 'Delete':
        delete(values)
    elif event == 'Copy':
        copy(values)
    elif event == 'Paste':
        paste(values, new_destination)
    elif event == 'Tag':
        tag(db=db, cursor=cursor, name_of_file=hashed_filename, filename=filename, values=values)
    elif event == "-TAG LIST-":
        tag_list(cursor=cursor, values=values, db=db, name_of_file=hashed_filename)
    if file_chosen:
        tag_check(cursor=cursor,name_of_file=hashed_filename, window=window)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break