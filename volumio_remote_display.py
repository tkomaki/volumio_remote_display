import os
import sys
import requests
import json
import tkinter.font
import urllib.request
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO





class Volumio:

    status = ""
    titile = ""
    artist = ""
    album = ""
    albumart_url = ""

    def __init__(self):
        args = sys.argv
        volumio_url = 'http://' + args[1]
        self.url = volumio_url
    
    def set_volumio_var_from_api(self):
        response = requests.get(self.url + "/api/v1/getState")

        json_data = response.json()
        self.status = json_data["status"]
        self.title = json_data["title"]
        self.artist = json_data["artist"]
        self.album = json_data["album"]
        self.albumart_url = self.url + json_data["albumart"]
        


## set background color
bgcolor = "cyan4"

## set text color
fgcolor = "white"


window = Tk()
window.title("Volumio Remote Display")
window.geometry('1000x1000')
window.configure(bg=bgcolor)
window.attributes("-fullscreen", True)



font_size = tkinter.font.Font(
    window,
    family="System",
    size=35,
)

font_size_bold = tkinter.font.Font(
    window,
    family="System",
    size=35,
    weight="bold"
)

font_smallsize = tkinter.font.Font(
    window,
    family="System",
    size=20,
    weight="bold"
)


## set label
vl = Volumio()
vl.set_volumio_var_from_api()

volumio_status = StringVar()
label_volumio_status = Label(
    window,
    textvariable=volumio_status,
    background=bgcolor,
    foreground='medium spring green',
    font=font_smallsize,
)

volumio_artist_album = StringVar()
label_volumio_artist_album = Label(
    window,
    textvariable=volumio_artist_album,
    background=bgcolor,
    foreground='white',
    font=font_smallsize,
)

volumio_title = StringVar()
label_volumio_title = Label(
    window,
    textvariable=volumio_title,
    background=bgcolor,
    foreground='medium spring green',
    font=font_size_bold,
)
     

raw_data = urllib.request.urlopen(vl.albumart_url).read()
img = Image.open(BytesIO(raw_data))
img = img.resize((500,500))
albumart = ImageTk.PhotoImage(img)
label_volumio_albumart = Label(
    window,
    image=albumart,
)


def output_to_window():

    def write_volumio(label_volumio_status, label_volumio_artist_album, label_volumio_title, label_volumio_albumart):
        label_volumio_title.grid(column=0,row=0)
        label_volumio_albumart.grid(column=0,row=2)
        label_volumio_artist_album.grid(column=0,row=1)
        label_volumio_status.grid(column=0,row=3)

        vl = Volumio()
        vl.set_volumio_var_from_api()
     
     
        volumio_status.set(str(vl.status))
        volumio_artist_album.set(str(vl.artist) + " / " + str(vl.album))
        volumio_title.set(str(vl.title))
     
        
        raw_data = urllib.request.urlopen(vl.albumart_url).read()
        img = Image.open(BytesIO(raw_data))
        img = img.resize((500,500))
        albumart = ImageTk.PhotoImage(img)
     
        label_volumio_albumart.configure(image=albumart)
        label_volumio_albumart.image = albumart



    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=1)
    window.rowconfigure(3, weight=1)


    write_volumio(label_volumio_status, label_volumio_artist_album, label_volumio_title, label_volumio_albumart)
 

    ## 10000 = 10 second
    window.after(10000,lambda: output_to_window())


output_to_window()

try:
    window.mainloop()
except:
    sys.exit("Error exit")



