#!/usr/bin/python
#encoding: utf-8

from Tkinter import *
import Tkinter
from genericpath import exists
import sqlite3


top = Tkinter.Tk()

categorias = ("No hay BD",)
muestra = Spinbox(top,values=categorias)

def listarCallBack(sql):
    lista = Toplevel()
    barra = Scrollbar(lista)
    texto = Text(lista)
    
    #TODO este es el que tiene que cambiar:
    texto.insert(INSERT,sql)
    
    
    texto.pack(side = LEFT, fill = BOTH)
    barra.pack(side = RIGHT, fill = Y)
    barra.config( command = texto.yview )
    lista.mainloop()
    
def buttCallBack():
    m= muestra.get()
    sql="SELECT * from PRODUCTOS WHERE CATEGORIA LIKE '%"+m+"%'"
    listarCallBack(sql)
    
butt=Tkinter.Button(top, text="buscar", command = buttCallBack)


def mostrar():
    butt.pack(side=RIGHT)
    muestra.pack(side = RIGHT)


def almacenar():
    conn = sqlite3.connect('comida.db')
    conn.execute('''DROP TABLE IF EXISTS PRODUCTOS''')
    conn.execute('''CREATE TABLE PRODUCTOS
         (CATEGORIA           TEXT    NOT NULL);''')
        
    
almacenar = Tkinter.Button(top, text="Almacenar", bd = 2, command=almacenar)
listar = Tkinter.Button(top, text="Mostrar Categoría",command=mostrar, bd= 2)

almacenar.pack( side = LEFT )
listar.pack( side = LEFT )
top.mainloop()