#encoding: utf-8

import Tkinter
import sqlite3
import tkMessageBox

from bs4 import BeautifulSoup
from pattern.db import LEFT
import requests


def donothing():
    print "a"

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
#            print p
            partido = p.get("title")
            print partido
            jornada = i
            print jornada
            resultado = p.find("span",{"class":"resultado"}).get_text()
            print resultado
            cronica = p.get("href")
            print cronica
            conn.execute("INSERT INTO CRONICAS VALUES(?,?,?,?);",(partido,i,resultado,cronica))
     
    cursor = conn.execute("SELECT COUNT(*) FROM CRONICAS")
    number=0
    for c in cursor:
        number=c[0]
     
    conn.commit()
    tkMessageBox.showinfo( "Informacion", "Numero de elementos en la BD: "+str(number))
    
    conn.close()



def principal():
    top = Tkinter.Tk()    

    
    

    

    a = Tkinter.Button(top, text="Almacenar", command = cargar)
    bc = Tkinter.Button(top, text="Goles", command= donothing)

    a.pack( side = LEFT )
    bc.pack( side = LEFT )
    top.mainloop()


if __name__=="__main__":
    principal()