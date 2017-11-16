#encoding: utf-8

import Tkinter
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup
import requests #pip install requests
from numpy.f2py.crackfortran import previous_context

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
         (CATEGORY         TEXT    NOT NULL,
         NOMBRE            TEXT     NOT NULL,
         lINK           TEXT     NOT NULL,
         PRICE           TEXT    NOT NULL,
         OLDPRICE        TEXT);''')
    cursor = conn.execute("SELECT * FROM CATEGORIAS")
    
    for row in cursor:
        r=requests.get(row[1])
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        
        paginas=soup.find("ul",{"class","pagination"})
        lastPage=1
        if paginas != None:
            lastPage = int(paginas.get_text()[-1])
        current=1
        while current<=lastPage:
            url = row[1]+u'?p='+str(current).decode('utf8')
            r=requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, "lxml")
     
            productos = soup.find_all("div",{"class","prod_wrap"})
            for p in productos:
                link = p.find("div",{"class","prod_name"}).find("a")
                nombre = link.get_text()
                link = link["href"]
                price = p.find("span",{"class","product_preu"})
                old_price = price.find("del")
                if old_price != None:
                    previous_price=old_price.get_text()
                    real_price=price.get_text().replace(previous_price,"")
                else:
                    previous_price=0.0
                    real_price=price.get_text()
                conn.execute("INSERT INTO PRODUCTOS VALUES(?,?,?,?,?);",(row[0],nombre,link,real_price, previous_price))
            current+=1
    
    conn.commit()
    conn.close()
    tkMessageBox.showinfo( "Informacion", "Base de Datos creada correctamente")
    
def mostar_categoria():
    lc=[]
    conn = sqlite3.connect('comida.db')
    cursor = conn.execute("SELECT TITLE FROM CATEGORIAS")
    for cc in cursor:
        lc.append(cc[0])
    
    categorias = tuple(lc)
    new = Tkinter.Toplevel()
    
    spin = Spinbox(new,values=categorias)
    
    text = Tkinter.Listbox(new, width=100, height=20, selectmode= EXTENDED)
    scrollbar = Tkinter.Scrollbar(new)
    
    butt=Tkinter.Button(new, text="buscar", command= lambda: search(spin.get(), text))
    
    butt.pack(side=RIGHT)
    spin.pack(side = RIGHT)
    
    text.pack(side = LEFT, fill = BOTH)
    scrollbar.pack( side = RIGHT, fill=Y )
    scrollbar.config( command = text.yview )
    
    new.mainloop()
    conn.close()

def search(categoria, text):
    conn = sqlite3.connect('comida.db')
    cursor = conn.execute("SELECT * FROM PRODUCTOS WHERE CATEGORY LIKE '%"+categoria+"%'")
    text.delete(0, END)  #.curselection()
    i=1
    for row in cursor:
        text.insert(i,"Producto: "+row[1].strip()+"\n")
        text.insert(i+1,"Precio: "+row[3]+"\n")
        i+=2
    
    conn.close()


top = Tkinter.Tk()
 
AC = Tkinter.Button(top, text ="Almacenar Categorias", command=almacenar_productos)
MC = Tkinter.Button(top, text ="Mostrar Categoria", command=mostar_categoria)
 
AC.pack( side = LEFT )
MC.pack( side = LEFT )
top.mainloop()