import PySimpleGUI as sg
from tag_layout import tagging_layout
from search_layout import search_layout
import sqlite3
from search_functions import *
from tag_functions import *
hashed_filename: str
filename: str
file_chosen=False
# layout =[
#     [
#         sg.TabGroup(
#             [sg.Tab('Tag Images',tl)],
#             [sg.Tab('Search Images', sl)]
#         )
#     ]
# ]
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
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # # Fetch all the table names
    # tables = cursor.fetchall()
    # print(tables)


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
        hashed_filename, filename, file_chosen = file_list(window=window,values=values)
    elif event == 'Tag':
        results = tag(db=db, cursor=cursor, name_of_file=hashed_filename, filename=filename, values=values)
    elif event == "-TAG LIST-":
        tag_list(cursor=cursor, values=values, db=db, name_of_file=hashed_filename)
    # if file_chosen:
    #     tag_check(cursor=cursor,name_of_file=hashed_filename, window=window)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break