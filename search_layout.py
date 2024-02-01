from email.mime import image
import PySimpleGUI as sg
from PIL import Image, ImageTk
import sqlite3
# from main import db, window, event, values
import io
import tkinter as tk
import os 

imgdata=None


# right_click_menu = ['&Right', ['Move', 'Rename', 'Delete']]

search_column=[
    [sg.Text("Search Images"),
     sg.In(size=(40,1),enable_events=True,key="-SEARCH-"),
     sg.B('Search')],
    [sg.Listbox(values=["tagged images"],enable_events=True,size=(40,20),key="-IMAGE LIST-", right_click_menu=right_click_menu)]
]
#do a check every beginning if the pics in the locations do exist

image_column=[

    [sg.Text("Choose an image from list on left:")],

    [sg.Text(size=(40, 1), key="-IMAGE OUTPUT-")],

    [sg.Image(key="-SEARCHED IMAGE-", data=imgdata, size=(300,300))],
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
