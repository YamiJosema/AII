#encoding:utf-8
from Tkinter import *
from datetime import datetime
import os
import tkMessageBox

from whoosh import qparser
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser, MultifieldParser, GtLtPlugin


dircorr="Docs\Correos"
diragend="Docs\Agenda"
dirindexC="Index/Correos"
dirindexA="Index/Agenda"
#Crea un indice desde los documentos contenidos en dirdocs
#El indice lo crea en un directorio (dirindex)
def cargar():
    correos = cargar_correos() 
    agenda = cargar_agenda()
    
    tkMessageBox.showinfo("Fin de indexado", "Se han indexado "+str(correos)+ " correos\nSe han indexado "+str(agenda)+" contactos")
    
def cargar_correos():
    if not os.path.exists(dircorr):
        print "Error: no existe el directorio de documentos: "+dircorr
    else:
        if not os.path.exists(dirindexC):
            os.mkdir(dirindexC)
    
    schema= Schema(remitente=TEXT(stored=True), destinatarios=KEYWORD(stored=True), fecha=DATETIME, asunto=TEXT(stored=True), contenido=TEXT, file=TEXT(stored=True))
    ixc = create_in(dirindexC, schema)
    writer = ixc.writer()
    i=0
    for docname in os.listdir(dircorr):
        if not os.path.isdir(dircorr+docname):
            add_doc(writer, dircorr, docname)
            i+=1
    writer.commit()
    
    return i
    
def cargar_agenda():
    if not os.path.exists(diragend):
        print "Error: no existe el directorio de documentos: "+diragend
    else:
        if not os.path.exists(dirindexA):
            os.mkdir(dirindexA)
    schema = Schema(email=TEXT,nombre=TEXT(stored=True))
    ixa = create_in(dirindexA, schema)
    writer = ixa.writer()
    i=0
    for docname in os.listdir(diragend):
        with open(diragend+"/"+docname, 'r') as outfile:
            lines = outfile.readlines()
            for i in range(0, len(lines)/2):
                writer.add_document(email=unicode(lines[i]),nombre=unicode(lines[i+1]))
            
    writer.commit()
    
    return len(lines)/2

    
def buscar_contenido():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ixc=open_dir(dirindexC)      
        with ixc.searcher() as searcher:
            query = MultifieldParser(["asunto", "contenido"], ixc.schema).parse(unicode(en.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END,get_agenda(r['remitente']))
                lb.insert(END,r['asunto'])
                lb.insert(END,'')
     
    v = Toplevel()
    v.title("Busqueda por Contenido")
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

def buscar_fecha():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        try:
            fecha = datetime.strptime(en.get(), '%Y%m%d').date()
            ixc=open_dir(dirindexC)      
            with ixc.searcher() as searcher:
                query = QueryParser("fecha", ixc.schema).parse(unicode(fecha)) #posteriores a una fecha dada fechaCorreo>fechaDada
                print query
                results = searcher.search(query)
                for r in results:
                    lb.insert(END,r['remitente'])
                    lb.insert(END,r['destinatarios'])
                    lb.insert(END,r['asunto'])
                    lb.insert(END,'')
        except:
            lb.insert(END, "Fecha erronea")
     
    v = Toplevel()
    v.title("Busqueda por Fecha")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca fecha (YYYYMMDD):")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set, width=80, height=40)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview)

def buscar_spam():
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ixc=open_dir(dirindexC)      
        with ixc.searcher() as searcher:
            query = QueryParser("asunto", ixc.schema, group=qparser.OrGroup).parse(unicode(en.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END,r['file'])
                lb.insert(END,'')
     
    v = Toplevel()
    v.title("Busqueda de span")
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text="Introduzca palabras clave:")
    l.pack(side=LEFT)
    en = Entry(f)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set, width=80, height=40)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview)

def get_agenda(email):
    nombre = email
    ixa = open_dir(dirindexA)
    with ixa.searcher() as searcher:
        query = QueryParser("email", ixa.schema).parse(unicode(email))
        results = searcher.search(query)
        for r in results:
            nombre = r['nombre']
    return nombre  
    
         
def add_doc(writer, path, docname):
    fileobj=open(path+'\\'+docname, "rb")
    # IMPORTANTE: Convertir el contenido del fichero a Unicode
    rte=unicode(fileobj.readline().strip())
    dtos=unicode(fileobj.readline().strip())
    fch=unicode(datetime.strptime(fileobj.readline().strip(), '%Y%m%d').date())
    ast=unicode(fileobj.readline().strip())
    ctdo=unicode(fileobj.read())
    fileobj.close()
    
    writer.add_document(remitente=rte, destinatarios=dtos, fecha=fch, asunto=ast, contenido=ctdo, file=unicode(docname))

    # print "Creado indice para fichero " + docname
    
def ventana_principal():
    top = Tk()
    indexar = Button(top, text="Indexar", command = cargar)
    indexar.pack(side = TOP)
    BuscarC = Button(top, text="Buscar por Contenido", command = buscar_contenido)
    BuscarC.pack(side = TOP)
    BuscarF = Button(top, text="Buscar por Fecha", command = buscar_fecha)
    BuscarF.pack(side = TOP)
    BuscarS = Button(top, text="Buscar Spam", command = buscar_spam)
    BuscarS.pack(side = TOP)
    top.mainloop()


if __name__ == '__main__':
    ventana_principal()