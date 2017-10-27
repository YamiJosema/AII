#encoding: utf-8

import Tkinter
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup
import requests #pip install requests
from numpy.f2py.crackfortran import previous_context

def datos():
    conn = sqlite3.connect('eventos.db')
    conn.execute('''DROP TABLE IF EXISTS CATEGORIAS''')
    conn.execute('''CREATE TABLE CATEGORIAS
         (NAME         TEXT    NOT NULL,
         lINK           TEXT     NOT NULL,
         CATEGORY        TEXT    NOT NULL);''')
    
    url = "http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp"
    r=requests.get(url)
    data = r.text


top = Tkinter.Tk()
 
D = Tkinter.Button(top, text ="Datos")
B = Tkinter.Button(top, text ="Buscar")
E = Tkinter.Button(top, text ="Estadisticas") 

D.pack( side = LEFT )
B.pack( side = LEFT )
E.pack( side = LEFT )
top.mainloop()