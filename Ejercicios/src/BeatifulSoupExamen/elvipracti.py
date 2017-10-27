#encoding: utf-8

import Tkinter
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup
import requests #pip install requests
from numpy.f2py.crackfortran import previous_context

def donothing():
    print "hola"

top = Tkinter.Tk()
 
menubar = Menu(top)

dm = Menu(menubar, tearoff=0)
dm.add_command(label="Cargar", command=donothing)
dm.add_command(label="Mostrar", command=donothing)
dm.add_command(label="Salir", command=donothing)
menubar.add_cascade(label="Datos", menu=dm)

bm = Menu(menubar, tearoff=0)
bm.add_command(label="Tema", command=donothing)
bm.add_command(label="Autor", command=donothing)
bm.add_command(label="Fecha", command=donothing)

menubar.add_cascade(label="Buscar", menu=bm)

em = Menu(menubar, tearoff=0)
em.add_command(label="Temas más populares", command=donothing)
em.add_command(label="Temas más activos", command=donothing)
menubar.add_cascade(label="Estadísticas", menu=em)


top.config(menu=menubar)

D = Tkinter.Button(top, text ="Datos")
B = Tkinter.Button(top, text ="Buscar")
E = Tkinter.Button(top, text ="Estadisticas") 

top.mainloop()