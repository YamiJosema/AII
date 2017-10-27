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


def lista():
    conn = sqlite3.connect('derecho.db')
#    cursor = conn.execute("SELECT * from TEMAS")

    lista = Toplevel()
    barra = Scrollbar(lista)
    lista = Listbox(lista,width=150,height=40)
    
    i = 0
    #TODO este es el que tiene que cambiar:
 #   for row in cursor:
    while i < 3:
        i+=1
#        lista.insert(i,row[0]+"   Autores: "+row[2]+"  Fecha: "+row[3])
        lista.insert(i,"HOLA!")
        
    lista.pack(side = LEFT, fill = BOTH)
    barra.pack(side = RIGHT, fill = Y)
    barra.config( command = lista.yview )
    lista.mainloop()
    conn.close()

def mostrar():
    lista("SELECT * from TEMAS")


def principal():
    top = Tkinter.Tk()
     
    menubar = Menu(top)
    
    dm = Menu(menubar, tearoff=0)
    dm.add_command(label="Cargar", command=donothing)
    dm.add_command(label="Mostrar", command=mostrar)
    dm.add_command(label="Salir", command=top.destroy)
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
    
if __name__=="__main__":
    principal()