'''
Created on 27 oct. 2017

@author: Josema
'''

#encoding: utf-8

import Tkinter
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup
import requests #pip install requests
from numpy.f2py.crackfortran import previous_context

def almacenar():
    almacenar_categorias()
    almacenar_eventos()
    tkMessageBox.showinfo( "Informacion", "Base de Datos creada correctamente")

def almacenar_categorias():
    conn = sqlite3.connect('eventos.db')
    conn.execute('''DROP TABLE IF EXISTS CATEGORIAS''')
    conn.execute('''CREATE TABLE CATEGORIAS
         (NAME         TEXT    NOT NULL,
         lINK           TEXT     NOT NULL,
         CATEGORY        TEXT    NOT NULL);''')
    
    url = "http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp"
    r=requests.get(url)
    data = r.text
    
    soup = BeautifulSoup(data, "lxml")
#     table = soup.find("table").find("tr").find_next_sibling().find("table").find("td").find("table")
    table = soup.find("font",{"class":"TituloIndice"}).parent.parent.parent.find_all("td")
    category=""
    name=""
    link=""
    for c in table:
        children = c.contents
        if children[0].name == "font":
            category = children[0].next_sibling.get_text()
        else:
            atag = c.find("a")
            if atag!=None:
                name = atag.get_text()
                link = atag['href']
                conn.execute("INSERT INTO CATEGORIAS VALUES(?,?,?);",(name,link, category))
    conn.commit()
    conn.close()
    
def almacenar_eventos():
    conn = sqlite3.connect('eventos.db')
    conn.execute('''DROP TABLE IF EXISTS EVENTOS''')
    conn.execute('''CREATE TABLE EVENTOS
         (TITLE         TEXT    NOT NULL,
         DATE           TEXT     NOT NULL,
         AREA            TEXT    NOT NULL);''')
    
    url = "http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp"
    r=requests.get(url)
    data = r.text
    
    soup = BeautifulSoup(data, "lxml")
#     table = soup.find("table").find("tr").find_next_sibling().find("table").find("td").find("table")
    fechas = soup.find_all("span",{"class":"Sala"})
    cuerpo = soup.find_all("th",{"class":"Destacamos"})
    
    for i in range(len(fechas)):
        date = fechas[i].get_text()
        title = cuerpo[i].find("font").get_text()
        areas = cuerpo[i].find("p").find_next_siblings()
        area=""
        for a in areas:
            area+=a.get_text()
        conn.execute("INSERT INTO EVENTOS VALUES(?,?,?);",(title, date,area))
    
    conn.commit()
    conn.close()


def buscar_categoria():
    search = Tkinter.Toplevel()
    
    var = Tkinter.StringVar()
    label = Label( search, textvariable=var, relief=RAISED )
    var.set("Introduzca categoria: ")
    label.pack(side = LEFT)
     
    category = Entry(search, bd =5)
    category.pack(side = LEFT)
     
    b = Button(search, text="Buscar", width=10, command= lambda: buscarC(category.get()))
    b.pack(side = LEFT)
    
def buscarC(category):
    sql = "SELECT * FROM CATEGORIAS WHERE CATEGORY LIKE '%"+category+"%'"
    conn = sqlite3.connect('eventos.db')
    cursor = conn.execute(sql)

    lista = Tkinter.Toplevel()

    text = Tkinter.Text(lista)
    
    for row in cursor:
        text.insert(INSERT,"Evento: "+row[0]+", "+row[2]+"\n")
        text.insert(INSERT,row[1]+"\n\n")
    
    scrollbar = Tkinter.Scrollbar(lista)
    
    text.pack(side = LEFT, fill = BOTH)
    scrollbar.pack( side = RIGHT, fill=Y )
    scrollbar.config( command = text.yview )
    
    lista.mainloop()
    conn.close()

def buscar_evento():
    search = Tkinter.Toplevel()
    
    var = Tkinter.StringVar()
    label = Label( search, textvariable=var, relief=RAISED )
    var.set("Introduzca palabra clave: ")
    label.pack(side = LEFT)
     
    keyword = Entry(search, bd =5)
    keyword.pack(side = LEFT)
     
    b = Button(search, text="Buscar", width=10, command= lambda: buscarE(keyword.get()))
    b.pack(side = LEFT)
    
def buscarE(keyword):
    sql = "SELECT * FROM EVENTOS WHERE TITLE LIKE '%"+keyword+"%' OR AREA LIKE '%"+keyword+"%'"
    conn = sqlite3.connect('eventos.db')
    cursor = conn.execute(sql)

    lista = Tkinter.Toplevel()

    text = Tkinter.Text(lista)
    
    for row in cursor:
        text.insert(INSERT,"Evento: "+row[0]+"\n")
        text.insert(INSERT,"Fecha: "+row[1]+"\n\n")
    
    scrollbar = Tkinter.Scrollbar(lista)
    
    text.pack(side = LEFT, fill = BOTH)
    scrollbar.pack( side = RIGHT, fill=Y )
    scrollbar.config( command = text.yview )
    
    lista.mainloop()
    conn.close()


top = Tkinter.Tk()
 
AC = Tkinter.Button(top, text ="Almacenar", command= almacenar)
BC = Tkinter.Button(top, text ="Buscar Categoria", command= buscar_categoria)
BE = Tkinter.Button(top, text ="Buscar Evento", command=buscar_evento) 

AC.pack( side = LEFT )
BC.pack( side = LEFT )
BE.pack( side = LEFT )
top.mainloop()