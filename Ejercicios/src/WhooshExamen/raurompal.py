'''
Created on 17 nov. 2017

@author: elvir
'''

import Tkinter
from Tkinter import *
import tkMessageBox
from bs4 import BeautifulSoup
import requests #pip install requests
import os
from whoosh.index import *
from whoosh.fields import *
from whoosh.qparser import QueryParser
from datetime import datetime, timedelta

dirindexP = "Index/Partidos"
dirindexC = "Index/Cronicas"


def cargar():
    if not os.path.exists(dirindexP):
        os.mkdir(dirindexP)
    schema = Schema(numerojor=TEXT(stored=True), local=TEXT, visitante=TEXT, resultado=TEXT)  # importante poner stored si vas a listar
    ixr = create_in(dirindexP, schema)

    if not os.path.exists(dirindexC):
        os.mkdir(dirindexC)
    schema = Schema(fecha=DATETIME(stored=True), autor=TEXT, titular=TEXT(stored=True), title=TEXT(stored=True),
                    text=TEXT(stored=True))  # importante poner stored si vas a listar
    ixc = create_in(dirindexC, schema)

def principal():
    top = Tkinter.Tk()

    menubar = Menu(top)

    im = Menu(menubar, tearoff=0)
    im.add_command(label="Cargar", command=cargar)
    im.add_command(label="Salir", command=top.destroy)
    menubar.add_cascade(label="Datos", menu=im)

    tm = Menu(menubar, tearoff=0)
    tm.add_command(label="Noticia", command=lambda: buscar("title", dirindexT))
    tm.add_command(label="Fecha", command=lambda: buscar("author", dirindexT))
    tm.add_command(label="Autor", command=lambda: buscar("author", dirindexT))
    bm = Menu(menubar, tearoff=0)
    bm.add_cascade(label="Buscar", menu=tm)

    top.config(menu=menubar)

    top.mainloop()


if __name__ == "__main__":
    principal()