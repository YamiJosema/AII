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


def lista(sql):
    conn = sqlite3.connect('derecho.db')
#    cursor = conn.execute(sql)

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

def autor():
    conn = sqlite3.connect('noticias.db')
    busqueda = Toplevel()
    label= Label(busqueda, text="Introduzca el autor:")
    entrada=Entry(busqueda, bd=5)

    def buttCallBack():
        m=entrada.get()
        sql="SELECT * from TEMAS WHERE AUTOR LIKE '%"+m+"%'"
        lista(sql)
    
    butt=Tkinter.Button(busqueda, text="buscar", command = buttCallBack)
    label.pack(side=LEFT)
    entrada.pack(side=LEFT)
    butt.pack(side=LEFT)
    
    
    busqueda.mainloop()
    conn.close()


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
    bm.add_command(label="Autor", command=autor)
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