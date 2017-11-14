import Tkinter
from Tkinter import *
import tkMessageBox
from bs4 import BeautifulSoup
import requests #pip install requests
import os
from whoosh.index import *
from whoosh.fields import *
from whoosh.qparser import QueryParser

dirindexT="Index/Themes"
dirindexR="Index/Answers"

def cargar():
    if not os.path.exists(dirindexT):
        os.mkdir(dirindexT)
    schema = Schema(title=TEXT(stored=True),link=TEXT,respuestas=TEXT,visitas=TEXT,author=TEXT(stored=True),link2=TEXT,date=TEXT(stored=True)) #importante poner stored si vas a listar
    ixt = create_in(dirindexT,schema)
    
    if not os.path.exists(dirindexR):
        os.mkdir(dirindexR)
    schema = Schema(title=TEXT(stored=True),date=TEXT(stored=True),textarea=TEXT(phrase=True),author=TEXT(stored=True),link=TEXT) #importante poner stored si vas a listar. pharase si quieres buscar por frases
    ixa = create_in(dirindexR,schema)
    
    count = 0
    answ = 0
    
    url = "https://foros.derecho.com/foro/20-Derecho-Civil-General/"
    r=requests.get(url)
    data = r.text
    
    soup = BeautifulSoup(data, "lxml")
    temas = soup.find_all("li",{"class":"threadbit"})
    
    writer=ixt.writer()
    for t in temas:
        first=t.find("h3",{"class":"threadtitle"})
        title = first.find("a").get_text()
        link = first.find("a")["href"]
        
        answ+=cargarR("https://foros.derecho.com/"+link, title, ixa)
      
        second = t.find("ul",{"class":"threadstats"})
        res=second.find("a").get_text().strip()
        vis=second.get_text().split("\n")[2].replace("Visitas: ", "")
        
        third=t.find("span",{"class":"time"}).parent
        date = third.get_text().strip()
        au = t.find("a",{"class":"username"})
        linkAutor = au['href']
        autor=au.get_text()
            
        writer.add_document(title=unicode(title),link=unicode(link),respuestas=unicode(res),visitas=unicode(vis),author=unicode(autor),link2=unicode(linkAutor),date=unicode(date))
            
        count+=1
    writer.commit() 
    tkMessageBox.showinfo( "Informacion", "Numero de temas: "+str(count)+ "\nNumero de respuestas: "+str(answ))

def cargarR(url, titleT, ix):
    count = 0
    
    r=requests.get(url)
    data = r.text
    
    soup = BeautifulSoup(data, "lxml")
    temas = soup.find_all("li",{"class":"postbitlegacy"})
    
    writer=ix.writer()
    for t in temas:
        first=t.find("div",{"class":"posthead"})
        date = first.find("span",{"class":"date"}).get_text()
        
        core = t.find("div",{"class":"postdetails"})
        
        second = core.find("div",{"class":"userinfo"})
        aZone=second.find("a",{"class":"username"})
        author = aZone.get_text()
        link = aZone['href']
        
        third = core.find("div",{"class":"postbody"})
        text = third.find("div",{"class":"content"}).get_text().strip()
        
        writer.add_document(title=unicode(titleT),date=unicode(date),textarea=unicode(text),author=unicode(author),link=unicode(link))
                    
        count+=1
    writer.commit() 
    
    return count
    
def buscar(pattern, index):
    def mostrar_lista(event):  #preguntar porque es necesaria esta variable
        lb.delete(0,END)  
        ix=open_dir(index)      
        with ix.searcher() as searcher:
            query = QueryParser(pattern, ix.schema).parse(unicode(en.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END,r['title'])
                lb.insert(END,r['date'])
                lb.insert(END,r['author'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda")
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
    
def principal():
    top = Tkinter.Tk()
     
    menubar = Menu(top)
    
    im = Menu(menubar, tearoff=0)
    im.add_command(label="Indexar", command=cargar)
    im.add_command(label="Salir", command=top.destroy)
    menubar.add_cascade(label="Inicio", menu=im)
    
    tm = Menu(menubar, tearoff=0)
    tm.add_command(label="Titulo", command=lambda: buscar("title", dirindexT))
    tm.add_command(label="Autor", command=lambda: buscar("author", dirindexT))
    bm = Menu(menubar, tearoff=0)
    bm.add_cascade(label="Tema",menu=tm)
    
    rm = Menu(menubar, tearoff=0)
    rm.add_command(label="Texto", command=lambda: buscar("textarea", dirindexR))
    bm.add_cascade(label="Respuestas", menu=rm)
    
    menubar.add_cascade(label="Buscar", menu=bm)
    
    top.config(menu=menubar)
    
    top.mainloop()
    
if __name__=="__main__":
    principal()