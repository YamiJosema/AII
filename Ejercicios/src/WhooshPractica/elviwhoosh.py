#encoding:utf-8
from Tkinter import Menu
import Tkinter
import os
import tkMessageBox

from bs4 import BeautifulSoup
import requests
from whoosh.fields import Schema, TEXT, DATETIME
from whoosh.index import create_in


def donothing():
    print "jaja si soi io er chocu"

def index():
    schema=Schema(titulo=TEXT(stored=True), linktema=TEXT, username=TEXT(stored=True), linkuser=TEXT, texto=TEXT(stored=True), fecha=TEXT)

    if not os.path.exists("index"):
        os.mkdir("index")
    ix = create_in("index", schema)
    writer = ix.writer()
    count = 0
    
    for i in range(1,4,1):
        url = "https://foros.derecho.com/foro/20-Derecho-Civil-General/page"+str(i) 
        r=requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        temas = soup.find_all("li",{"class":"threadbit"})
        for t in temas:
            first=t.find("h3",{"class":"threadtitle"})
            
            title = first.find("a").get_text()
            link = "https://foros.derecho.com/"+first.find("a")["href"]
        
            second = t.find("ul",{"class":"threadstats"})
            
            res=second.find("a").get_text().strip()
            vis=second.get_text().split("\n")[2].replace("Visitas: ", "")
        
            third=t.find("span",{"class":"time"}).parent
            
            date = third.get_text().strip()
            autor = t.find("a",{"class":"username"}).get_text()
            autorlink = "https://foros.derecho.com/"+t.find("a",{"class":"username"})["href"]
            
            r=requests.get(link)
            data = r.text
            soup = BeautifulSoup(data, "lxml")
            texto = soup.find("blockquote").get_text().strip()
            print title + "\n" + date + "\n" + autor + "\n" + link + "\n" + autorlink + "\n" + texto + "\n AAAAAAAAAAAA" "\n" 
            writer.add_document(titulo=unicode(title), linktema=unicode(link), username=unicode(autor), linkuser=unicode(autorlink), texto=unicode(texto), fecha=unicode(date))
            count+=1

    
    
    tkMessageBox.showinfo( "Informacion", "Numero de elementos: "+str(count))


def principal():
    
    top = Tkinter.Tk()
    menubar = Menu(top)
    im = Menu(menubar,tearoff=0) 
    im.add_command(label= "Indexar",command = index)
    im.add_command(label= "Salir", command = top.destroy)
    menubar.add_cascade(label="Inicio", menu=im)
    
    bm = Menu(menubar,tearoff=0)
    
    tbm = Menu(bm,tearoff=0)
    tbm.add_command(label= "Titulo",command = donothing)
    tbm.add_command(label= "Autor", command = donothing)
    bm.add_cascade(label= "Temas", menu = tbm)
    rbm = Menu(bm,tearoff=0)
    rbm.add_command(label= "Texto",command = donothing)
    bm.add_cascade(label= "Respuestas", menu = rbm)
    menubar.add_cascade(label="Buscar", menu = bm)
    top.config(menu= menubar)
    
    
    top.mainloop()

    
    


if __name__ == "__main__":
    principal()