import os
import io
import PySimpleGUI as sg
import shutil

new_destination=None
copied_files:str=[]
previous_action:str=None
class file_manager_functions:
    def __init__(self, copied_files):
        self.copied_files = copied_files
        self.previous_action=None

    def move(cls, path, values):
        cls.copy(path, values)
        cls.previous_action="copy"
        # delete(values)
        #move is just copy and delete. so probably just do that. 

    def rename(cls,current_path,values):
        
        new_name = sg.popup_get_text("Enter new name:", default_text=values)
        print(new_name)
        print(values)
        if new_name:
            os.rename(os.path.join(current_path,values),os.path.join(current_path,new_name))
        return os.path.join(current_path,new_name)

    def sort():
        return None

    def delete(cls,path, values):
        #needs the file location 
        for f in values:
            file=os.path.join(path,f)
            os.remove(file)
        sg.popup(f"{values} successfully deleted")


    def copy(cls,path, values):
        cls.copied_files=[]
        for i, f in enumerate(values):
            file=os.path.join(path, f)
            cls.copied_files.append(file)
        print(cls.copied_files)
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

    def paste(cls,new_destination):
        #only show up if move or copy is called
        # from looking at the file manager, they still show up the paste value, but the paste option
        # is disabled. 
        #need to do the new destination thing
        # i guess for now, do something "for file in values, shutil copy into new destination?"
        
        try:
            for file in cls.copied_files:
                shutil.copy(file,new_destination)
            
                if previous_action=="move":
                    cls.delete(file)
            cls.copied_files=[]
            cls.previous_action=None

        except IOError as e:
            print(f"Error copying file: {e}")
        return None
