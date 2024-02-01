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
f1 = file_manager_functions(files=[])
current_clicked_item = None
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
#resetting the table function
delete_table = "DROP TABLE IF EXISTS images"
cursor.execute(delete_table)
db.commit()
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
        search_image_list(window=window, values = values["-IMAGE LIST-"])
    elif event=="-FOLDER-":
        current_path=open_folder(window=window, values=values)
    elif event == "-FILE LIST-":
        element=window.find_element_with_focus()       
        path=values["-FILE LIST-"][0]
        full_path=os.path.join(current_path,path)
        filename=full_path
        file_chosen=True
        # if handle_double_click(path):
        file_type=identify_path(full_path)
        if file_type=="File":
        #check if chosen file is folder. if chosen file is folder, then 
        #proceed and redo the get_file_list thing.
            hashed_filename, filename, file_chosen=file_list(window=window,folder=current_path, filename=path)
        elif file_type=="Folder":
            if handle_double_click(path):
            #do a separate one. where if the folder is chosen, it would show a new 
            #set of files
                full_path=full_path.replace("\\",'/')
                window["-FILE LIST-"].update(get_file_list(full_path))
                current_path=full_path
                window["-FOLDER-"].update(full_path)
        
    elif event=='Move':
        f1.files=[]
        #maybe something like appending the file paths
        # file_path = values["-FOLDER-"]
        # for i,f in enumerate():
        #     absolute_file=os.path.join(current_path, f)
        #     files.append(absolute_file)
        
        f1.move(current_path,values["-FILE LIST-"])
    elif event =='Rename':
        path = values["-FILE LIST-"][0]
        renamed_file=f1.rename(current_path,path)
        window["-FILE LIST-"].update(get_file_list(current_path))
        #update the database
        rename_query="SELECT location FROM images where image_name = ?"
        cursor.execute(rename_query,(hashed_filename,))
        result = cursor.fetchone()
        if result:
            #so i guess check the database contents, then change that part??
            # so maybe something like update the location
            files = ast.literal_eval(result[0])
            file_array=[]
            for file in files:
                if file == os.path.join(current_path,path):
                    file_array.append(renamed_file)
                else:
                    file_array.append(file)
            update_query="UPDATE images SET location=? where image_name=?;"

            cursor.execute(update_query, (str(file_array), hashed_filename))
            db.commit()
    elif event == 'Delete':  
        f1.files=[]
            # for f in files:
            #     if f not in filename:
            #         file_array.append(f)
        files_to_delete=[item for item in values['-FILE LIST-']]
        print(files_to_delete)
        f1.delete(files_to_delete=files_to_delete, base_path=current_path, cursor=cursor, db=db, action="delete")        
        window["-FILE LIST-"].update(get_file_list(current_path))

    elif event == 'Copy':
        # for i,f in enumerate(values["-FILE LIST-"]):
        #     absolute_file=os.path.join(current_path, f)
        #     files.append(abso0lute_file)
        #check if the entry exists in the database. 
        f1.files=[]
        f1.copy(current_path,values["-FILE LIST-"])
    elif event == 'Paste':
        f1.paste(current_path,db)
        window["-FILE LIST-"].update(get_file_list(current_path))
        
        #this should work now. now i need to see whether the users have chosen copy or cut before. 
        # i only really need to check if they chose move before
        #i guess something like         
    elif event == 'Tag':
        tag(db=db, cursor=cursor, name_of_file=hashed_filename, filename=filename, values=values)
        file_chosen=True
    elif event == "-TAG LIST-":
        if handle_double_click(values['-TAG LIST-']):
            tag_list(cursor=cursor, values=values['-TAG LIST-'][0], db=db, name_of_file=hashed_filename) 

        window["-TAG LIST-"].update
    if file_chosen:
        tag_check(cursor=cursor,name_of_file=hashed_filename, window=window)
        file_chosen = False
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
