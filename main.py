import PySimpleGUI as sg
from tag_layout import tagging_layout
from search_layout import search_layout
import sqlite3
from search_functions import *
from tag_functions import *
from file_checks import *
hashed_filename: str
filename: str
file_chosen=False

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

    #check if the photo is in the database. 
    #we can try the md5sum 
    #check what happens first
    #print the name of the file
    
    #check if file exists in the local database

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

# check all the image locations if the images are located at those positions

# get all the entry of the database
cursor.execute("SELECT * FROM images")    
# entries = cursor.fetchall()
# for entry in entries:
#     #check if the file exists in the location we are expecting
#     hash = entry[0]
#     location=entry[2]
#     if os.path.isfile(location):
#         continue
#     else:
#         new_path = find_file_by_hash(hash)
#         cursor.execute("UPDATE images SET location=? WHERE image_name=?",(new_path,hash))


hashed_filename=""
current_driver="C:/"
while True:

    event, values = window.read()
    # search functions
    if event == "Search":
        search(values=values, db = db, window=window)
    elif event =="-IMAGE LIST-":
        search_image_list(window=window, values = values)
    elif event=="-FOLDER-":
        open_folder(window=window, values=values)
    elif event == "-FILE LIST-":
        path=values["-FILE LIST-"]
        print(path)
        full_path=os.path.join(current_driver,path[0])
        print(full_path)
        file_type=identify_path(full_path)
        print(file_type)
        if file_type=="File":
        #check if chosen file is folder. if chosen file is folder, then 
        #proceed and redo the get_file_list thing.
            hashed_filename, filename, file_chosen = file_list(window=window,values=values)
        elif file_type=="Folder":
            #do a separate one. where if the folder is chosen, it would show a new 
            #set of files
            window["-FILE LIST-"].update(get_file_list(full_path))
            current_driver=full_path
    elif event == 'Tag':
        tag(db=db, cursor=cursor, name_of_file=hashed_filename, filename=filename, values=values)
    elif event == "-TAG LIST-":
        tag_list(cursor=cursor, values=values, db=db, name_of_file=hashed_filename)
    if file_chosen:
        tag_check(cursor=cursor,name_of_file=hashed_filename, window=window)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break