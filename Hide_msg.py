import cv2
import numpy as np
import os
import tkinter
import PIL
from PIL import ImageTk, Image
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter.filedialog import askopenfilenames
import time
from tkinter import filedialog

path=''
def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")


def encode(image_name, secret_data):
    # read the image
    image = cv2.imread(image_name)
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", n_bytes)
    value.insert('0.0','[*] Maximum bytes to encode:%s\n'%n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    value.insert(END,'\n[*] Encoding data...')
    # add stopping criteria
    secret_data += "#####"
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    
    
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    
    
    return image
    



def decode(image_name):
    print("[+] Decoding...")
    value.delete('0.0',END)
    # read the image
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]

    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####":
            break
    value.insert(END,'\n[+] Decoding...\n')
    return decoded_data[:-5]
def load_image():
    global msg_file
    msg_file=msg_file
    file=askopenfilenames(initialdir = "/",title = "Select file for encode",filetypes = [("PNG file","*.png"),('GIF files','*.gif')])
    print(file[0])
    global path
    global panel
    global but
    path=file[0]
    #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    panel.destroy()
    but.destroy()
    pkk=PIL.Image.open(path).resize((300,300), PIL.Image.ANTIALIAS)
    
    img = ImageTk.PhotoImage(pkk)
    

    #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    but=ttk.Button(bottomframe,text='Hide message in this image',command=hide)
    but.pack()
    #global panel
   # panel = tkinter.Label(bottomframe,text='not suported',image='')
    panel = tkinter.Label(bottomframe,text='not suported',image=img)
    panel.image= img
    

    #The Pack geometry manager packs widgets in rows or columns.
    panel.pack( padx=10 )
    
    
def load_file():
    try:
        file=askopenfilenames(initialdir = "/",title = "Select file",filetypes = [("TXT file","*.txt")])
        print(open(file[0],'r').read())
        value.delete('0.0',END)
        value.insert('0.0',open(file[0],'r').read())
    except IndexError:pass
    
    

def hide():
    inputValue=value.get("1.0","end-1c")
    print(inputValue)
    value.delete('0.0',END)
    input_image = path
    output_name=path.split('.')
    dd=output_name[0]+'_encoded'
    das=dd+'.'+output_name[-1]
    global output_image
    output_image = das
    secret_data = inputValue
    # encode the data into the image
    encoded_image = encode(image_name=input_image, secret_data=secret_data)
    # save the output image (encoded image)
    cv2.imwrite(output_image, encoded_image)
    # decode the secret data from the image
    #decoded_data = decode(output_image)
    value.insert(END,'\nyour message was hiden in %s'%output_image)
    
    #print("[+] Decoded data:", decoded_data)
def open_txt():
    value.delete('0.0',END)
    but.config(text='please wait')
    decoded_data = decode(path)
    print("[+] Decoded data:", decoded_data)
    value.insert(END,'{msg}>>> '+decoded_data)
    but.configure(text='Open message from this image')

def decode_img():
    #encode_image.destroy()
    msg_file.destroy()
    file=askopenfilenames(initialdir = "/",title = "Select file for decode",filetypes = [("PNG file","*.png"),('GIF files','*.gif')])
    print(file[0])
    global path
    global panel
    global but
    path=file[0]
    #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    panel.destroy()
    but.destroy()
    pkk=PIL.Image.open(file[0]).resize((300,300), PIL.Image.ANTIALIAS)
    
    img = ImageTk.PhotoImage(pkk)
    

    #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    but=ttk.Button(bottomframe,text='Open message from this image',command=open_txt)
    but.pack()
    #global panel
   # panel = tkinter.Label(bottomframe,text='not suported',image='')
    panel = tkinter.Label(bottomframe,text='not suported',image=img)
    panel.image= img
    print('not in path',path)
    panel.pack()
output_image = ''
win=tkinter.Tk()
win.title('Hide Or Open Text In Image (made by somen)')
panel=tkinter.Label(win,image='')
but=ttk.Button(win)
bottomframe = Frame(win,width=5,bg='white',bd=3)
bottomframe.grid(row=1,column=0)
bottomframee = Frame(win,bg='green')
bottomframee.grid(row=1,column=1)
lbl=ttk.Label(bottomframe,text='TO hide your secret message \ntype into this box Then click on "hide message in this image button\nyou can select a txt file by clicking on "Load message from a file"button \n\n But first click on "Load Your image "\n\n To Decode Image click on "Decode an image" button \n then click on "Open message from this image" Button')
lbl.pack(side=TOP)

encode_image=ttk.Button(bottomframe,text='click to encode your image',command=load_image)
encode_image.pack()
msg_file=ttk.Button(bottomframee,text='Load message from a file',command=load_file)
msg_file.pack(side= TOP)
ttk.Button(bottomframee,text='click to Decode an Image',command=decode_img).pack()
value=tkinter.Text(bottomframee,height=25.5,width=60,wrap=WORD)
value.pack()





#Start the GUI




win.mainloop()
