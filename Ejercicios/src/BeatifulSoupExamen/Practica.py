#encoding: utf-8

import Tkinter
from Tkinter import *
import tkMessageBox
import sqlite3
from bs4 import BeautifulSoup
import requests #pip install requests
from numpy.f2py.crackfortran import previous_context

def cargar():
    for i in range(4):
        url = "https://foros.derecho.com/foro/20-Derecho-Civil-General/page"+str(i)
        cargar_pagina(url)
    conn = sqlite3.connect('derecho.db')
    cursor = conn.execute("SELECT COUNT(*) FROM TEMAS")
    
    number=0
    for c in cursor:
        number=c[0]
        print number
    
    tkMessageBox.showinfo( "Informacion", "Numero de elementos: "+str(number))


def cargar_pagina(url):
    conn = sqlite3.connect('derecho.db')
    conn.execute('''DROP TABLE IF EXISTS TEMAS''')
    conn.execute('''CREATE TABLE TEMAS
         (TITLE         TEXT    NOT NULL,
         lINK           TEXT     NOT NULL,
         AUTOR        TEXT    NOT NULL,
         DATE        TEXT    NOT NULL,
         RES        TEXT    NOT NULL,
         VIS        TEXT    NOT NULL);''')
    
    url = "https://foros.derecho.com/foro/20-Derecho-Civil-General"
    r=requests.get(url)
    data = r.text
    
    soup = BeautifulSoup(data, "lxml")
    temas = soup.find_all("li",{"class":"threadbit"})
    
    for t in temas:
        first=t.find("h3",{"class":"threadtitle"})
        title = first.get_text()
        link = first.find("a")["href"]
        
        second = t.find("ul",{"class":"threadstats"})
        res=second.find("a").get_text()
        vis=second.get_text().split("\n")[2].replace("Visitas: ", "")
        
        third=t.find("span",{"class":"time"}).parent
        date = third.get_text().strip()
        autor = t.find("a",{"class":"username"}).get_text()
        
        conn.execute("INSERT INTO TEMAS VALUES(?,?,?,?,?,?);",(title,link,autor,date,res,vis))
    
    conn.commit()
    conn.close()


top = Tkinter.Tk()
 
C = Tkinter.Button(top, text ="Cargar", command=cargar)
M = Tkinter.Button(top, text ="Mostrar")
S = Tkinter.Button(top, text ="Salir") 

C.pack( side = LEFT )
M.pack( side = LEFT )
S.pack( side = LEFT )
top.mainloop()