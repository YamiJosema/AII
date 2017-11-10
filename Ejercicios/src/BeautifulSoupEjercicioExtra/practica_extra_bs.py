#encoding: utf-8

from Tkconstants import  RIGHT, TOP, BOTH, Y, END
from Tkinter import  Label, Spinbox, Frame, Scrollbar, Listbox
import Tkinter
import sqlite3
import tkMessageBox

from bs4 import BeautifulSoup
from pattern.db import LEFT
import requests


def cargar():
    conn = sqlite3.connect('marca.db')
    conn.execute('''DROP TABLE IF EXISTS CRONICAS''')
    conn.execute('''CREATE TABLE CRONICAS
         (PARTIDO         TEXT    NOT NULL,
         JORNADA        TEXT    NOT NULL,
         RESULTADO        TEXT    NOT NULL,
         CRONICA        TEXT    NOT NULL);''')
    
    url = "http://www.marca.com/futbol/primera-division/calendario.html"
    r=requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    soup.get("section")
    contenedor = soup.find("ul",{"class":"contenedor-calendario"})

    jornadas = contenedor.findAll("li",{"class":"contenedorCalendarioInt"})
    for j in jornadas:
        i = j.find("h2").get_text().replace('Jornada ', '')
        partidos = j.findAll("a",{"class":"final"})
        for p in partidos:
            partido = p.get("title")
            resultado = p.find("span",{"class":"resultado"}).get_text()
            cronica = p.get("href")
            conn.execute("INSERT INTO CRONICAS VALUES(?,?,?,?);",(partido,i,resultado,cronica))    
     
    cursor = conn.execute("SELECT COUNT(*) FROM CRONICAS")
    number=0
    for c in cursor:
        number=c[0]
     
    conn.commit()
    conn.close()

    number2 = insertarpartidos()
    tkMessageBox.showinfo( "Informacion", str(number)+ " cronicas y "+str(number2)+" goles.")
    

def insertarpartidos():
    conn = sqlite3.connect('marca.db')
    
    conn.execute('''DROP TABLE IF EXISTS GOLES''')
    conn.execute('''CREATE TABLE GOLES
         (EQUIPO        TEXT    NOT NULL,
         JUGADOR         TEXT    NOT NULL,
         MINUTO        TEXT    NOT NULL,
         CRONICA        TEXT    NOT NULL);''')
    
    cursor = conn.execute("SELECT CRONICA FROM CRONICAS")
    
    for url in cursor:
        cronica = url[0]
        r=requests.get(cronica)
        data = r.text
        soup = BeautifulSoup(data, "lxml").find("div",{"class":"marcador"})
        insertaequipo(conn,soup.find("div",{"class":"equipo-1"}),cronica)
        insertaequipo(conn,soup.find("div",{"class":"equipo-2"}),cronica)

    conn = sqlite3.connect('marca.db')
    cursor = conn.execute("SELECT COUNT(*) FROM GOLES")
    number=0
    for c in cursor:
        number=c[0]
     
    conn.commit()
        
    conn.close()
    return number

def insertaequipo(conn,soup,cronica):
    
    equipo = soup.find("h3").get_text()
    for gol in soup.findAll("li"):
        gol.span.extract()
        textos = gol.get_text().replace("p.","").replace("p.p.","").replace("(p)","").replace("(pp)","").replace(".","").replace("()","").replace("')","")
        textos = textos.split("(")
        jugador = textos[0].lstrip()
        minuto = textos[1]
        conn.execute("INSERT INTO GOLES VALUES(?,?,?,?);",(equipo,jugador,minuto,cronica))
    conn.commit()

            
def buscar():
    conn = sqlite3.connect('marca.db')
    root = Tkinter.Toplevel()
    frame = Frame(root)
    frame2 = Frame(root)
    
    
    cursor = conn.execute("SELECT PARTIDO from CRONICAS")
    
    partidos = []
    for c in cursor:
        partidos.append(c[0])

    def cambio():   
        cursor = conn.execute("SELECT CRONICA FROM CRONICAS WHERE PARTIDO LIKE '"+partido.get()+"'")
        for row in cursor:
            sql = "SELECT * FROM GOLES WHERE CRONICA LIKE '%"+row[0]+"%'"
        
        cursor = conn.execute(sql)
        lista.delete(0,END)
        i = 0
        for row in cursor:
            i+=1
            lista.insert(i,"EQUIPO: "+row[0]+"        JUGADOR: "+row[1]+"       MINUTO: "+row[2])
          
    partido = Spinbox(frame,values = partidos, command =cambio)    
    etiq = Label(frame,text="Elija Partido:") 
    barra = Scrollbar(frame2)
    lista = Listbox(frame2,width=80,height=8)
    

    
    frame.pack( side = LEFT )
    frame2.pack(side = LEFT)
    lista.pack(side = LEFT, fill = BOTH)
    barra.pack(side = RIGHT, fill = Y)
    barra.config( command = lista.yview )
        
    etiq.pack( side = TOP )
    partido.pack(side = RIGHT )

    root.mainloop()

def principal():
    top = Tkinter.Tk()    


    a = Tkinter.Button(top, text="Almacenar", command = cargar)
    bc = Tkinter.Button(top, text="Goles", command= buscar)

    a.pack( side = LEFT )
    bc.pack( side = LEFT )
    top.mainloop()


if __name__=="__main__":
    principal()