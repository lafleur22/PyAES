#------------------------------------------ MODULES ----------------------------------------------------------

from Cryptodome.Cipher import AES
from tkinter import *
from tkinter import ttk
from tkinterdnd2 import *
from tkinter import filedialog as fd
from tkinter import messagebox
from hashlib import md5
import time
from threading import *

#------------------------------------------- VARIABLES --------------------------------------------------------

fileList=[]
toggle="ENC"

#-------------------------------------------- FUNCTIONS -------------------------------------------------------

def encrypt(key, data):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext

def decrypt(key, data):
    nonce = data[:AES.block_size]
    tag = data[AES.block_size:AES.block_size * 2]
    ciphertext = data[AES.block_size * 2:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def select_file():    
    filetypes = (  ('All files', '*.*'),('All files', '*.*')) 
    filenames = fd.askopenfilenames(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    for fichero in filenames:  
        fileList.append(fichero)

    for indice in range (len(fileList)):
        lbox.insert(indice, fileList[indice])
        
    return filenames

def cambiaModo():
    global toggle

    if toggle=="ENC":
        labelMode.config(bg="red",text="DECRYPT FILES")
        buttonAccept['text'] = 'DECRYPT'
        toggle="DEC"
    else:
        labelMode.config(bg="light blue",text="ENCRYPT FILES")
        buttonAccept['text'] = 'ENCRYPT'
        toggle="ENC"

def barra():
    global root
    root.update_idletasks()
    pbar.start()
    root.update_idletasks()

def begin():
    key=entryPassword.get()
    if entryPassword.get()=="":
            messagebox.showinfo('INFO','Password needed')
            pbar.stop()
            pbar.place_forget()
            return
    if len(fileList)==0:
            messagebox.showinfo('INFO','No files selected')
            pbar.stop()
            pbar.place_forget()
            return

    if toggle=="ENC":   
        for fich in fileList:
            with open(fich,"rb") as fr:
                    data = fr.read()
                    hashedkey = md5(key.encode('utf8')).digest()
                    encdata=encrypt(hashedkey,data)
            with open(fich+".aes", "wb") as binary_file:
                    binary_file.write(encdata)                        
        messagebox.showinfo('INFO','File(s) encrypted')
        for indice in range (len(fileList)):
            lbox.delete(indice, END)  
            fileList.clear() 
        entryPassword.delete(0, END) 
        pbar.stop()
        pbar.place_forget()
    if toggle=="DEC":    
       
        for fich in fileList:
            try:

                with open(fich,"rb") as fr:
                    data = fr.read()
                    hashedkey = md5(key.encode('utf8')).digest()
                    encdata=decrypt(hashedkey,data)    
                    name = fich[:-4]
                with open(name, "wb") as binary_file:
                    binary_file.write(encdata)
            except:
                messagebox.showinfo('INFO','Wrong password')
                pbar.stop()
                pbar.place_forget()
                return                    
        messagebox.showinfo('INFO','File(s) Decrypted')  
        for indice in range (len(fileList)):
            lbox.delete(indice, END)  
        fileList.clear() 
        entryPassword.delete(0, END)
        pbar.stop()
        pbar.place_forget()

def hilo():
    pbar.place(x=1,y=1)
    pbar.start()

    t1=Thread(target=begin, daemon = True)
    t1.start()
    


#------------------------------------------------ WINDOW -------------------------------------------------------------------

root=Tk()
root.title("AES Encryptor")
root.resizable(False,False)
root.geometry("800x400+100+100")

labelMode=Label(root,text="ENCRYPT FILES")
labelMode.config(background="light blue",justify="center")
labelMode.place(x=5,y=5,width=790,height=30)

buttonChangueMode=Button(root,text="Changue mode",command=(cambiaModo))
buttonChangueMode.place(x=694,y=7)

buttonSelectFiles=Button(root,text="Select files",command=(select_file))
buttonSelectFiles.place(x=10,y=50)

lbox = Listbox(root)
lbox.place(x=10,y=80,width=270,height=300)

labelPassword=Label(root,text="Password:")
labelPassword.place(x=310,y=80)

entryPassword=Entry(root)
entryPassword.place(x=400,y=81,width=220)

frame1=Frame(root)
frame1.place(x=350,y=200,width=360,height=200)

pbar = ttk.Progressbar(frame1,orient='horizontal',mode='indeterminate',length=350)

buttonAccept=Button(root,text="ENCRYPT",command=(hilo))
buttonAccept.place(x=640,y=76,width=130)

root.mainloop()