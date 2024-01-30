import ast
from email.mime import image
import PySimpleGUI as sg
from PIL import Image, ImageTk
import sqlite3
# from main import db, window, event, values
import io
import tkinter as tk
from search_layout import *
import os
from file_checks import format

imgdata=None

def convert_image_to_bytes(image):
    img_byte_array=io.BytesIO()
    image.save(img_byte_array, format='PNG')
    return img_byte_array.getvalue()

def search(values, db, window):
# if event=="Search":
    # I think at startup, check all the images available, and then check if the md5sum matches. do this later. 
    #check all the tags with the 
    #we will search for the image
    # anyways, now that we are here, 
    # probably have a set of images?
    input=values["-SEARCH-"]
    print(values)
    input_array=input.split(" ")
    print(input_array) 
    tag_query: str
    for index, item in enumerate(input_array):

        if index == 0:
            tag_query=f"tags LIKE '%{item}%'"
        else:
            tag_query=f'{tag_query} AND tags LIKE \'%{item}%\''
        # tag_query=f"{tag_query} tags LIKE '%{item}%'"
    search_query=f"SELECT location from images WHERE {tag_query}"
    print(search_query)
    cur = db.cursor()
    cur.execute(search_query)
    results=cur.fetchall()
    all_files=[]
    print(results)
    for i, f in enumerate(results):
        files = ast.literal_eval(f[0])
        for file in files:
            all_files.append(file)

    #for each results, show the location of the stuff. 
    window["-IMAGE LIST-"].update(all_files)
    # for index, item in enumerate(results):
def search_image_list(window, values):
# elif event=="-IMAGE LIST-":
    filename=values[0]
    print(filename)
    pil_image=Image.open(filename)
    img_bytes=convert_image_to_bytes(pil_image)
    window["-SEARCHED IMAGE-"].update(data=img_bytes)

    #and then execute the entry.
    #search all tags with all of the same inputs 
    # check the database if the image has all the tags in the input

