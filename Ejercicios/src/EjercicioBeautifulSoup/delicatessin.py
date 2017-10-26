#encoding: utf-8

import Tkinter
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup
import requests #pip install requests


def listarCallBack(sql):
    conn = sqlite3.connect('comida.db')
    cursor = conn.execute(sql)

    lista = Toplevel()
    barra = Scrollbar(lista)
    lista = Listbox(lista,width=150,height=40)
    
    i = 0
    #TODO este es el que tiene que cambiar:
    for row in cursor:
        i+=1
        if not row[4]=="0.0":
            lista.insert(i,row[1]+"    "+row[3]+"OFERTA!!!  Antes: "+row[4])
        else:
            lista.insert(i,row[1]+"    "+row[3])
        
    lista.pack(side = LEFT, fill = BOTH)
    barra.pack(side = RIGHT, fill = Y)
    barra.config( command = lista.yview )
    lista.mainloop()
    conn.close()


def mostrar_boton_buscar():
    conn = sqlite3.connect('comida.db')

    busqueda = Toplevel()
    cursor = conn.execute("SELECT TITLE from CATEGORIAS")
    etiq = Label(busqueda,text="Elija Categoria:")

    categ = []
    for c in cursor:
        categ.append(c[0])


    tuple(categ)
    muestra = Spinbox(busqueda,values=categ)

    def buttCallBack(): 
        m=muestra.get()
        sql="SELECT * from PRODUCTOS WHERE TITLE LIKE '%"+m+"%'"
        listarCallBack(sql)
    
    butt=Tkinter.Button(busqueda, text="buscar", command = buttCallBack)
    etiq.pack(side=LEFT)

    muestra.pack(side=LEFT)

    butt.pack(side=LEFT)
   
    
    busqueda.mainloop()
    conn.close()


def almacenar_categoria():
    conn = sqlite3.connect('comida.db')
    conn.execute('''DROP TABLE IF EXISTS CATEGORIAS''')
    conn.execute('''CREATE TABLE CATEGORIAS
         (TITLE         TEXT    NOT NULL,
         lINK           TEXT     NOT NULL);''')
    
    url = "http://www.delicatessin.com/es/Delicatessin"
    r=requests.get(url)
    data = r.text
    
    soup = BeautifulSoup(data, "lxml")
    
    categ = soup.find("ul", {"class":"tree"}).find_all("a")
    
    categorias = []
    
    for c in categ:
        link = c["href"]
        title = c.get_text()
        
        
        conn.execute("INSERT INTO CATEGORIAS VALUES(?,?);",(title,link))
    
    
    categorias = tuple(categorias)    
    conn.commit()
    conn.close()
 

def almacenar_productos():
    almacenar_categoria()
    
    conn = sqlite3.connect('comida.db')
    conn.execute('''DROP TABLE IF EXISTS PRODUCTOS''')
    conn.execute('''CREATE TABLE PRODUCTOS
         (TITLE         TEXT    NOT NULL,
         NAME            TEXT    NOT NULL,
         lINK           TEXT     NOT NULL,
         PRICE           TEXT    NOT NULL,
         OLDPRICE        TEXT);''')
    cursor = conn.execute("SELECT * FROM CATEGORIAS")
    
    for row in cursor:
        r=requests.get(row[1])
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        
        productos = soup.find_all("div",{"class","prod_wrap"})
        for p in productos:
            link = p.find("div",{"class","prod_name"}).find("a")["href"]
            name = p.find("div",{"class","prod_name"}).find("a").get_text()
            price = p.find("span",{"class","product_preu"})
            old_price = price.find("del")
            if old_price != None:
                new_price=old_price.get_text()
                real_price=price.get_text().replace(new_price,"")
            else:
                new_price=0.0
                real_price=price.get_text()
            conn.execute("INSERT INTO PRODUCTOS VALUES(?,?,?,?,?);",(row[0],name,link,real_price, new_price))
    
    tkMessageBox.showinfo("Informacion", "Base de Datos creada correctamente")
    conn.commit()
    conn.close()

top = Tkinter.Tk()
        

butt=Tkinter.Button(top, text="buscar")

AC = Tkinter.Button(top, text ="Almacenar Categorias", command=almacenar_productos)
MC = Tkinter.Button(top, text ="Mostrar Categoria", command= mostrar_boton_buscar)
 
AC.pack( side = LEFT )
MC.pack( side = LEFT )

top.mainloop()