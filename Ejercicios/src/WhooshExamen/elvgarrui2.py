from Tkinter import *
import Tkinter
import tkMessageBox
from datetime import datetime

import os

from whoosh import qparser
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser, MultifieldParser, GtLtPlugin


from bs4 import BeautifulSoup
import requests

dirindex="Index"
autores= []

def get_schema():
    return Schema(jornada=TEXT(stored=True), local=TEXT(stored=True), visitante=TEXT(stored=True), resultado=TEXT(stored=True), fecha=DATETIME(stored=True), autor=TEXT(stored=True), titular=TEXT(stored=True), titulo=TEXT(stored=True), texto=TEXT)    

def index():
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    ix = create_in(dirindex,get_schema())
    
    writer=ix.writer()
    
    count = 0
    
    url = "http://www.marca.com/futbol/primera-division/calendario.html"
    r=requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    soup.get("section")
    contenedor = soup.find("ul",{"class":"contenedor-calendario"})

    jornadas = contenedor.findAll("li",{"class":"contenedorCalendarioInt"})
    
    
    for j in jornadas:
        #i = No. DE JORNADA
        i = j.find("h2").get_text().replace('Jornada ', '')
        
        partidos = j.findAll("a",{"class":"final"})
        for p in partidos:
            partido = p.get("title")
            nombres= partido.split(" vs ")
            local=nombres[0].strip()
            visitante=nombres[1].strip()
            resultado = p.find("span",{"class":"resultado"}).get_text().strip()
            #print resultado
            cronica = p.get("href").strip()
            rcronica=requests.get(cronica)
            datac = rcronica.text
            soup = BeautifulSoup(datac, "lxml")
            titulares=soup.find("section",{"class":"columnaTitular"})
            titular = titulares.h3
            titulo =  titulares.h4
            nombre = titulares.find("span",{"class","nombre"}).get_text()
            fecha = titulares.find("span",{"class","fecha"}).get_text()
            textos = soup.find("div",{"class":"cuerpo_articulo"}).find_all("p")
            texto=""
            for p in textos:
                texto+=p.get_text()+"  "
            
#             fch = datetime.strptime(unicode(fecha), '%Y%m%d')
            
            writer.add_document(jornada=unicode(i), local=unicode(local), visitante=unicode(visitante), resultado=unicode(resultado), fecha=datetime.utcnow(), autor=unicode(nombre), titular=unicode(titular), titulo=unicode(titulo), texto=unicode(texto))
            count+=1
        if int(i)==4:
            break
        
    writer.commit() 
    tkMessageBox.showinfo("Informacion", "Numero de partidos: "+str(count))
 
def buscar_noticia():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ixc=open_dir(dirindex)      
        with ixc.searcher() as searcher:
            query = QueryParser("texto", ixc.schema).parse(unicode(en.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END,r['jornada'])
                lb.insert(END,r['local'])
                lb.insert(END,'')
     
    v = Toplevel()
    v.title("Busqueda Noticias")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca palabra clave:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set, width=80, height=40)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview)    
    
def buscar(pattern):
    print "nada"

def principal():
    top = Tkinter.Tk()
    menubar = Menu(top)
    dm= Menu(menubar,tearoff=0)    
    dm.add_command(label = "Cargar",command=index)
    dm.add_command(label="Salir", command=top.destroy)
    menubar.add_cascade(label="Datos",menu=dm)

    bm= Menu(menubar,tearoff=0)
    bm.add_command(label = "Noticia", command= buscar_noticia)
    bm.add_command(label ="Fecha",command= lambda: buscar("fecha"))
    bm.add_command(label="Autor",command= lambda: buscar("autor"))
    menubar.add_cascade(label="Buscar",menu=bm)
    top.config(menu=menubar)
    top.mainloop()
    

if __name__ == '__main__':
    principal()