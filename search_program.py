from curses import window
from email.mime import image
import PySimpleGUI as sg
import sqlite3
imgdata=None

search_column=[[sg.Input(key="-SEARCH-"),
sg.B('Search')],
sg.ListBox(values="tagged images")]

show_image=[]

image_column=[

    [sg.Text("Choose an image from list on left:")],

    [sg.Text(size=(40, 1), key="-IMAGE OUTPUT-")],

    [sg.Image(key="-SEARCHED_IMAGE-", data=imgdata)],
]
tagging_layout = [
    [
        sg.Column(search_column),
        sg.VSeperator(),
        sg.Column(image_column),
    ]
]

window=sg.Window('Tag Searcher')


db=sqlite3.connect("./image_database.db", uri=True)
while True:
    event, values=window.read()
    if event=="Search":
        #we will search for the image
        # anyways, now that we are here, 
    if event==('Exit',sg.WIN_CLOSED):
        break
