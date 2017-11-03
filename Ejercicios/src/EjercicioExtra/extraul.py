#encoding: utf-8

import Tkinter
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup
import requests #pip install requests
from numpy.f2py.crackfortran import previous_context

def seleccionarJornada():
    auxiliar = Tkinter.Toplevel()
    partido = Spinbox(auxiliar, from_=0, to=10)
    butt = Tkinter.Button(auxiliar, text="Seleccionar")
    info = Listbox(auxiliar)
    info.insert("2")
    partido.pack(side = LEFT)
    butt.pack(side = LEFT)
    info.pack(side=LEFT)


    auxiliar.mainloop()

def principal():
    def buscarJornada():
        root = Tkinter.Toplevel()

        var = StringVar()
        label = Label(root, textvariable=var, relief=RAISED)

        var.set("Introduzca la jornada:")
        label.pack(side=LEFT)

        jornada = Entry(root, bd=5)
        jornada.pack(side=LEFT)

        boton = Button(root, text="Search", width=10, command=seleccionarJornada)
        boton.pack(side=LEFT)


    top = Tkinter.Tk()

    A = Tkinter.Button(top, text="Almacenar Categorias")
    BJ = Tkinter.Button(top, text="Buscar Categoria", command=buscarJornada)

    A.pack(side=LEFT)
    BJ.pack(side=LEFT)

    top.mainloop()


if __name__ == "__main__":
    principal()