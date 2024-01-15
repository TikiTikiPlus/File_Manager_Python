from email.mime import image
import PySimpleGUI as sg
import sqlite3
imgdata=None

search_column=[
    [sg.Text("Search Images"),
     sg.In(size=(40,1),enable_events=True,key="-SEARCH-"),
     sg.B('Search')],
    [sg.Listbox(values=["tagged images"],enable_events=True,size=(40,20),key="-IMAGE LIST-")]
]


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

window=sg.Window('Tag Searcher',tagging_layout)


db=sqlite3.connect("./image_database.db", uri=True)
while True:
    event, values=window.read()
    if event=="Search":
        print("lol")
        # I think at startup, check all the images available, and then check if the md5sum matches. do this later. 
        #check all the tags with the 
        #we will search for the image
        # anyways, now that we are here, 
        # probably have a set of images?
        input=values["-SEARCH-"][0]
        input_array=input.split()
        print(input_array) 
        tag_query: str
        for index, item in enumerate(input_array):
            if index == 0:
                tag_query=f"tags LIKE '%{item}%'"
            else:
                tag_query=f"{tag_query} AND tags LIKE '%{item}%'"
            tag_query=f"{tag_query} tags LIKE '%{item}%'"
        search_query=f"SELECT location from images WHERE {tag_query}"

        print(search_query) 
        #and then execute the entry.
        #search all tags with all of the same inputs 
        # check the database if the image has all the tags in the input
    elif event==('Exit',sg.WIN_CLOSED):
        break
