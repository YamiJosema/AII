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


def cargar():
    conn = sqlite3.connect('derecho.db')
    conn.execute('''DROP TABLE IF EXISTS TEMAS''')
    conn.execute('''CREATE TABLE TEMAS
         (TITLE         TEXT    NOT NULL,
         lINK           TEXT     NOT NULL,
         AUTOR        TEXT    NOT NULL,
         DATE        TEXT    NOT NULL,
         RES        TEXT    NOT NULL,
         VIS        TEXT    NOT NULL);''')
    
    for i in range(1,4,1):
        url = "https://foros.derecho.com/foro/20-Derecho-Civil-General/page"+str(i) 
        r=requests.get(url)
        data = r.text
    
        soup = BeautifulSoup(data, "lxml")
        temas = soup.find_all("li",{"class":"threadbit"})
    
        for t in temas:
            first=t.find("h3",{"class":"threadtitle"})
            title = first.find("a").get_text()
            link = first.find("a")["href"]
        
            second = t.find("ul",{"class":"threadstats"})
            res=second.find("a").get_text()
            vis=second.get_text().split("\n")[2].replace("Visitas: ", "")
        
            third=t.find("span",{"class":"time"}).parent
            date = third.get_text().strip()
            autor = t.find("a",{"class":"username"}).get_text()
        
            conn.execute("INSERT INTO TEMAS VALUES(?,?,?,?,?,?);",(title,link,autor,date,res,vis))
            conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM TEMAS")
    
    number=0
    for c in cursor:
        number=c[0]
    
    tkMessageBox.showinfo( "Informacion", "Numero de elementos: "+str(number))
    
    conn.close()


def lista(sql):
    conn = sqlite3.connect('derecho.db')
    cursor = conn.execute(sql)

    lista = Toplevel()
    barra = Scrollbar(lista)
    lista = Listbox(lista,width=150,height=40)
    
    i = 0
    #TODO este es el que tiene que cambiar:
    for row in cursor:
        i+=1
        lista.insert(i,"Titulo: "+row[0]+"     Autor: "+row[2]+"      Fecha: "+row[3])
        
    lista.pack(side = LEFT, fill = BOTH)
    barra.pack(side = RIGHT, fill = Y)
    barra.config( command = lista.yview )
    lista.mainloop()
    conn.close()

def mostrar():
    lista("SELECT * from TEMAS")

def autor():
    conn = sqlite3.connect('derecho.db')
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

def fecha():
    conn = sqlite3.connect('derecho.db')
    busqueda = Toplevel()
    label= Label(busqueda, text="Introduzca la fecha(dd/mm/yyyy):")
    entrada=Entry(busqueda, bd=5)

    def buttCallBack():
        m=entrada.get()
        sql="SELECT * from TEMAS WHERE DATE LIKE '%"+m+"%'"
        lista(sql)
    
    butt=Tkinter.Button(busqueda, text="buscar", command = buttCallBack)
    label.pack(side=LEFT)
    entrada.pack(side=LEFT)
    butt.pack(side=LEFT)
    
    
    busqueda.mainloop()
    conn.close()

def tema():
    conn = sqlite3.connect('derecho.db')
    busqueda = Toplevel()
    label= Label(busqueda, text="Introduzca palabra clave:")
    entrada=Entry(busqueda, bd=5)

    def buttCallBack():
        m=entrada.get()
        sql="SELECT * from TEMAS WHERE TITLE LIKE '%"+m+"%'"
        lista(sql)
    
    butt=Tkinter.Button(busqueda, text="buscar", command = buttCallBack)
    label.pack(side=LEFT)
    entrada.pack(side=LEFT)
    butt.pack(side=LEFT)
    
    
    busqueda.mainloop()
    conn.close()


def temasPopus():
    print "heh"

def principal():
    top = Tkinter.Tk()
     
    menubar = Menu(top)
    
    dm = Menu(menubar, tearoff=0)
    dm.add_command(label="Cargar", command=cargar)
    dm.add_command(label="Mostrar", command=mostrar)
    dm.add_command(label="Salir", command=top.destroy)
    menubar.add_cascade(label="Datos", menu=dm)
    
    bm = Menu(menubar, tearoff=0)
    bm.add_command(label="Tema", command=tema)
    bm.add_command(label="Autor", command=autor)
    bm.add_command(label="Fecha", command=fecha)
    
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