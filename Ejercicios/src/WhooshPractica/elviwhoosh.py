#encoding:utf-8
from Tkconstants import LEFT, END, RIGHT, TOP, Y, BOTH
from Tkinter import Menu, Entry, Label, Frame, Scrollbar, Listbox, Toplevel
import Tkinter
import os
import tkMessageBox

from bs4 import BeautifulSoup
import requests
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser


dirindex1="Index/Temas"
dirindex2="Index/Respuestas"

def donothing():
    print "boo!"

def index():
    schema=Schema(titulo=TEXT(stored=True), linktema=TEXT, username=TEXT(stored=True), linkuser=TEXT, res=TEXT,vis=TEXT, fecha=TEXT(stored=True))
    if not os.path.exists(dirindex1):
        os.mkdir(dirindex1)
    ix1 = create_in(dirindex1, schema)
    schema=Schema(titulo=TEXT(stored=True), fecha=TEXT(stored=True), username=TEXT(stored=True),linkuser=TEXT,texto=TEXT)
    if not os.path.exists(dirindex2):
        os.mkdir(dirindex2)
    ix2 = create_in(dirindex2, schema)
    
    
    writer = ix1.writer()
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
            
            results=second.find("a").get_text().strip()
            visits=second.get_text().split("\n")[2].replace("Visitas: ", "")
        
            third=t.find("span",{"class":"time"}).parent
            
            date = third.get_text().strip()
            autor = t.find("a",{"class":"username"}).get_text().strip()
            autorlink = "https://foros.derecho.com/"+t.find("a",{"class":"username"})["href"]
            
            r=requests.get(link)
            data = r.text
            soup = BeautifulSoup(data, "lxml")
#            print str(count) + ": "+title+"   //  "+autor
            writer.add_document(titulo=unicode(title).strip(), linktema=unicode(link).strip(), username=unicode(autor).strip(), linkuser=unicode(autorlink).strip(), res=unicode(results).strip(), vis=unicode(visits).strip(), fecha=unicode(date).strip())
            count+=1
            indexres(link,title,ix2)
    
    tkMessageBox.showinfo( "Informacion", "Numero de elementos: "+str(count))
    writer.commit()

def indexres(url,title,ix):
    r=requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    posts = soup.find_all("li",{"class":"postbitlegacy"})
    writer2 = ix.writer()

    for p in posts:
        
        date = p.find("span",{"class":"date"}).get_text()
        user = p.find("div",{"class":"username_container"})
        text = p.find("blockquote").get_text().strip()
        name = user.strong.get_text().strip()
        linkuser = "https://foros.derecho.com/"+user.a['href']
        writer2.add_document(titulo=unicode(title).strip(), fecha=unicode(date), username=unicode(name), linkuser=unicode(linkuser).strip(),texto=unicode(text))

    writer2.commit()

def buscar(pattern,index):
    def listar(event):
        lista.delete(0,END)
        ix=open_dir(index)
        with ix.searcher() as searcher:
            query = QueryParser(pattern,ix.schema).parse(unicode(entrada.get()))
            results= searcher.search(query)
            for r in results:
                lista.insert(END,r['titulo'])
                lista.insert(END,r['fecha'])
                lista.insert(END,r['username'])
                lista.insert(END,'')
                
    root = Tkinter.Toplevel()
    frame1=Frame(root)
    entrada=Entry(frame1,bd=2,width=60)
    lab = Label(frame1,text="Buscar: ")
    
    entrada.bind("<Return>",listar)
    sc=Scrollbar(root)
    sc.pack(side=RIGHT,fill=Y)
    lista=Listbox(root,yscrollcommand=sc.set)
    frame1.pack(side=TOP)

    lista.pack(side = TOP, fill = BOTH)
    lab.pack(side = LEFT)
    entrada.pack(side = LEFT)
    sc.config(command=lista.yview)
    root.mainloop()
    

    


def principal():
    
    top = Tkinter.Tk()
    menubar = Menu(top)
    im = Menu(menubar,tearoff=0) 
    im.add_command(label= "Indexar",command = index)
    im.add_command(label= "Salir", command = top.destroy)
    menubar.add_cascade(label="Inicio", menu=im)
    
    bm = Menu(menubar,tearoff=0)
    
    tbm = Menu(bm,tearoff=0)
    tbm.add_command(label= "Titulo",command = lambda: buscar("titulo",dirindex1))
    tbm.add_command(label= "Autor", command = lambda: buscar("username",dirindex1))
    bm.add_cascade(label= "Temas", menu = tbm)
    rbm = Menu(bm,tearoff=0)
    rbm.add_command(label= "Texto",command = lambda:buscar("texto",dirindex2))
    bm.add_cascade(label= "Respuestas", menu = rbm)
    menubar.add_cascade(label="Buscar", menu = bm)
    top.config(menu= menubar)
    
    
    top.mainloop()

    
    


if __name__ == "__main__":
    principal()