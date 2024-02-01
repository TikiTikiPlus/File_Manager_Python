import os
import io
import PySimpleGUI as sg
import shutil
import ast

new_destination=None
files:str=[]
previous_action:str=None
file_array:str=[]
class file_manager_functions:
    def __init__(self, files):
        self.files = files
        self.previous_action=None
        self.file_array=[]

    def move(cls, path, values):
        if os.path.exists(os.path.join(path,values[0])):
            cls.copy(path, values)
            cls.previous_action="move"
        # delete(values)
        #move is just copy and delete. so probably just do that. 

    def rename(cls,current_path,values):
        
        new_name = sg.popup_get_text("Enter new name:", default_text=values)
        if new_name:
            os.rename(os.path.join(current_path,values),os.path.join(current_path,new_name))
        return os.path.join(current_path,new_name)

    def sort():
        return None

#filename variable is used for checking the file to be deleted
    def delete(cls,base_path, files_to_delete, cursor, db, action=None):
        #needs the file location 
        if action == "delete":
            for f in files_to_delete:
                cls.copy(base_path, [os.path.basename(f)])
        sql_query = "SELECT * FROM images WHERE location LIKE ?;"
        print(cls.files)
        for f in cls.files:
            # f=f.replace('\\',\')
            print(f)
            cursor.execute(sql_query, ('%'+ f + '%',))
            
            result = cursor.fetchall()
            if result:
                db_files = ast.literal_eval(result[0][2])
                # file_array= [item for item in files if item.replace("\\\\",'\\') not in filename]
                # print(file_array)
                #file_array not being updated??
                cls.file_array = []
                print(cls.file_array)
                # f = f.replace('\\\\','\\')
                for item in db_files:
                    print("ITEM: " + item)
                    print("F: "+f)
                    # print(f"DB ITEM: {item}")
                    # print(f"FILE TO DELETE: {f}")
                    if f!=item:
                        cls.file_array.append(item)
                    else:
                        print("lol")
                print(cls.file_array)
                if len(cls.file_array)<1:
                    delete_entry="DELETE FROM images where location LIKE ?;"
                    cursor.execute(delete_entry,('%'+item+'%',))
                else:
                    update_array_query = "UPDATE images set location=? WHERE image_name = ?"
                    cursor.execute(update_array_query,(str(cls.file_array).replace("\\\\",'\\'),result[0][0]))
                db.commit()
            os.remove(f)


    def copy(cls,path, values):
        for i, f in enumerate(values):
            file=os.path.join(path, f)
            print(file)
            cls.files.append(file)
        print(cls.files)
        cls.previous_action="copy"
        # try:
        #     for file in values:
        #         print(file)
        #         copied_files.append(file)
        # except IOError as e: 
        #     print(f"Error copying file:{e}")

    """
    values (str list): this list contains the files to pasted
    new_destination (str): this string contains the destination where the files are to be
    placed.
    """

    def paste(cls,new_destination,db):
        #only show up if move or copy is called
        # from looking at the file manager, they still show up the paste value, but the paste option
        # is disabled. 
        #need to do the new destination thing
        # i guess for now, do something "for file in values, shutil copy into new destination?"
        cur = db.cursor()

        
        try:
            for file in cls.files:
                shutil.copy(file,new_destination)
                new_file=os.path.join(new_destination,os.path.basename(file))
                print("NEW FILE:"+ new_file)
                # file = file.replace("\\",'\\\\')
                print("OLD FILE:"+file)
                query = f"SELECT * from images WHERE location LIKE ? ;"
                cur.execute(query,('%' + file + '%',))
                result = cur.fetchall()
                print(result)
                if result:
                    hashed_filename =result[0][0]
                    # update_query="SELECT location FROM images where image_name=?"
                    # cur.execute(update_query,(file,))
                    # result=cursor.fetchone()
                    files=ast.literal_eval(result[0][2])
                    print(files)
                    files_lol=[item.replace("\\\\",'\\') for item in files]
                    # file_location=os.path.join(current_path, os.path.basename(filename))
                    # print(os.path.join(current_path, os.path.basename(filename)))
                    print(files_lol)
                    files_lol.append(new_file)
                    print(files_lol)
                    update_array_query = "UPDATE images SET location = ? WHERE image_name = ?;"
                    print((str(files_lol).replace("\\\\","\\")))
                    cur.execute(update_array_query, (str(files_lol).replace("\\\\","\\"), hashed_filename))
                # Commit the changes
                    db.commit()
                # result_array=[item.replace('\\\\\\\\', '\\') for item in result]
                    
            if cls.previous_action=="move":
                cls.delete(cursor=cur, db=db, action="move", base_path=None, files_to_delete=None)
            # if file in result:
                #     result.remove(file)
            cls.files=[]
            cls.previous_action=None
        
        except IOError as e:
            print(f"Error copying file: {e}")
        cur.close()
