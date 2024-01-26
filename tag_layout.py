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
from tag_functions import *


right_click_menu = ['&Right', ['Move', 'Rename','Delete', 'Copy', 'Paste']]
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
            values=get_file_list('/'), enable_events=True, size=(40, 20), key="-FILE LIST-",right_click_menu=right_click_menu
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
tagging_layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(tags_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]


#once the ui pops up, check the files in root. 

#then, can maybe expand from there? once that is done, we can possibly do tagging

#some with existing, and creating new tag option