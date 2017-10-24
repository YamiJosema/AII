#encoding: utf-8

import Tkinter
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup
import requests #pip install requests

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
    
    categorias = soup.find("ul", {"class":"tree"}).find_all("a")
    
    for c in categorias:
        link = c["href"]
        title = c.get_text()
        conn.execute("INSERT INTO CATEGORIAS VALUES(?,?);",(title,link))
    
    conn.commit()
    conn.close()

def almacenar_productos():
    almacenar_categoria()
    
    conn = sqlite3.connect('comida.db')
    conn.execute('''DROP TABLE IF EXISTS PRODUCTOS''')
    conn.execute('''CREATE TABLE PRODUCTOS
         (TITLE         TEXT    NOT NULL,
         lINK           TEXT     NOT NULL,
         PRICE           TEXT    NOT NULL,
         NEWPRICE        TEXT);''')
    cursor = conn.execute("SELECT * FROM CATEGORIAS")
    
    for row in cursor:
        r=requests.get(row[1])
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        
        productos = soup.find_all("div",{"class","prod_wrap"})
        for p in productos:
            link = p.find("div",{"class","prod_name"}).find("a")["href"]
            price = p.find("span",{"class","product_preu"})
            old_price = price.find("del")
            if old_price != None:
                new_price=old_price.get_text()
                real_price=price.get_text().replace(new_price,"")
            else:
                new_price=0.0
                real_price=price.get_text()
            conn.execute("INSERT INTO PRODUCTOS VALUES(?,?,?,?);",(row[0],link,real_price, new_price))
    
    tkMessageBox.showinfo( "Informacion", "Base de Datos creada correctamente")
        
top = Tkinter.Tk()
 
AC = Tkinter.Button(top, text ="Almacenar Categorias", command=almacenar_productos)
MC = Tkinter.Button(top, text ="Mostrar Categoria")
 
AC.pack( side = LEFT )
MC.pack( side = LEFT )
top.mainloop()