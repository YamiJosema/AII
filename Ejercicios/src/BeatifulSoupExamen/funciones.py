#encoding: utf-8

import Tkinter
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup
import requests #pip install requests
from numpy.f2py.crackfortran import previous_context

def buscarGeneral():
    new = Tkinter.Toplevel()

    BT = Tkinter.Button(new, text="Por Tema", command = buscarTitulo)
    BA = Tkinter.Button(new, text="Por Autor", command = buscarAutor)
    BF = Tkinter.Button(new, text="Por Fecha", command = buscarFecha)

    BT.pack(side=LEFT)
    BA.pack(side=LEFT)
    BF.pack(side=LEFT)

    new.mainloop()


def searchByTitulo(title, text):
    conn = sqlite3.connect('derecho.db')
    cursor = conn.execute("SELECT * FROM DERECHO WHERE TITLE LIKE '%" + title + "%'")
    text.delete(1, END)
    i = 1
    for row in cursor:
        text.insert(i, "Titulo: " + row[0].strip() + "\n")
        text.insert(i + 1, "Autor: " + row[2] + "\n")
        text.insert(i + 1, "Fecha: " + row[3] + "\n")
        i += 2

    conn.close()

def searchByAutor(autor, text):
    conn = sqlite3.connect('derecho.db')
    cursor = conn.execute("SELECT * FROM DERECHO WHERE AUTOR LIKE '%" + autor + "%'")
    text.delete(1, END)
    i = 1
    for row in cursor:
        text.insert(i, "Titulo: " + row[0].strip() + "\n")
        text.insert(i + 1, "Autor: " + row[2] + "\n")
        text.insert(i + 1, "Fecha: " + row[3] + "\n")
        i += 2

    conn.close()

def searchByFecha(fecha, text):
    conn = sqlite3.connect('derecho.db')
    cursor = conn.execute("SELECT * FROM DERECHO WHERE DATE LIKE '%" + fecha + "%'")
    text.delete(1, END)
    i = 1
    for row in cursor:
        text.insert(i, "Titulo: " + row[0].strip() + "\n")
        text.insert(i + 1, "Autor: " + row[2] + "\n")
        text.insert(i + 1, "Fecha: " + row[3] + "\n")
        i += 2

    conn.close()

def buscarTitulo():
    new = Tkinter.Toplevel()


    spin = Spinbox(new)

    text = Tkinter.Listbox(new, width=100, height=20, selectmode=EXTENDED)
    scrollbar = Tkinter.Scrollbar(new)

    butt = Tkinter.Button(new, text="buscar", command=lambda: searchByTitulo(spin.get(), text))

    butt.pack(side=RIGHT)
    spin.pack(side=RIGHT)

    text.pack(side=LEFT, fill=BOTH)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=text.yview)

    new.mainloop()

def buscarAutor():
    new = Tkinter.Toplevel()

    spin = Spinbox(new)

    text = Tkinter.Listbox(new, width=100, height=20, selectmode=EXTENDED)
    scrollbar = Tkinter.Scrollbar(new)

    butt = Tkinter.Button(new, text="buscar", command=lambda: searchByAutor(spin.get(), text))

    butt.pack(side=RIGHT)
    spin.pack(side=RIGHT)

    text.pack(side=LEFT, fill=BOTH)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=text.yview)

    new.mainloop()

def buscarFecha():
    new = Tkinter.Toplevel()

    spin = Spinbox(new)

    text = Tkinter.Listbox(new, width=100, height=20, selectmode=EXTENDED)
    scrollbar = Tkinter.Scrollbar(new)

    butt = Tkinter.Button(new, text="buscar", command=lambda: searchByFecha(spin.get(), text))

    butt.pack(side=RIGHT)
    spin.pack(side=RIGHT)

    text.pack(side=LEFT, fill=BOTH)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=text.yview)

    new.mainloop()

top = Tkinter.Tk()

D = Tkinter.Button(top, text="Cargar")
B = Tkinter.Button(top, text="Buscar", command = buscarGeneral)
E = Tkinter.Button(top, text="Estadisticas")

D.pack(side=LEFT)
B.pack(side=LEFT)
E.pack(side=LEFT)
top.mainloop()