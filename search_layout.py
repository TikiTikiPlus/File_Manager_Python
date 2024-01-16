from email.mime import image
import PySimpleGUI as sg
from PIL import Image, ImageTk
import sqlite3
# from main import db, window, event, values
import io
import tkinter as tk
imgdata=None

root = tk.Tk()
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()

size=(screen_width/2,screen_height/2)

root.destroy()



search_column=[
    [sg.Text("Search Images"),
     sg.In(size=(40,1),enable_events=True,key="-SEARCH-"),
     sg.B('Search')],
    [sg.Listbox(values=["tagged images"],enable_events=True,size=(40,20),key="-IMAGE LIST-")]
]
#do a check every beginning if the pics in the locations do exist

image_column=[

    [sg.Text("Choose an image from list on left:")],

    [sg.Text(size=(40, 1), key="-IMAGE OUTPUT-")],

    [sg.Image(key="-IMAGE-", data=imgdata,size=size)],
]
search_layout = [
    [
        sg.Column(search_column),
        sg.VSeperator(),
        sg.Column(image_column),
    ]
]

# window=sg.Window('Tag Searcher',search_layout)


# # db=sqlite3.connect("./tags_database.db", uri=True)
