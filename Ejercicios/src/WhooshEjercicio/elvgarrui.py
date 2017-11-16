from Tkconstants import RIGHT, Y, TOP, BOTH, LEFT, END
from Tkinter import Menu, Frame, Entry, Label, Scrollbar, Listbox
import Tkinter
import os
import tkMessageBox

from whoosh.fields import *
from whoosh.index import open_dir, create_in
from whoosh.qparser import *

from WhooshPractica.elviwhoosh import dirindex2
from whoosh.qparser.default import QueryParser


dirindex1 = "Index/Correos"
dirindex2= "Index/Agenda"
dirAgenda= "Docs/Agenda/agenda.txt"
dirCorreos= "Docs/Correos"

def index():
    schema = Schema(fichero=TEXT(stored=True),remitente=TEXT(stored=True),destinatario=KEYWORD(stored=True),fecha=DATETIME,asunto=TEXT(stored=True),cuerpo=TEXT)
    if not os.path.exists(dirindex1):
        os.mkdir(dirindex1)
    
    ix1= create_in(dirindex1,schema)
    schema=Schema(email=TEXT,nombre=TEXT(stored=True))
    if not os.path.exists(dirindex2):
        os.mkdir(dirindex2)
    ix2=create_in(dirindex2,schema)
    
    writer = ix2.writer()
    i=0
    j=0
    email=""
    with open(dirAgenda) as f:
        for line in f:
            if i==1:
                nombre = unicode(line.strip())
                writer.add_document(email=email,nombre=nombre)
#                print email +"  NOMBRE: "+nombre
                i=0
                j+=1
                
            else:
                email=unicode(line.strip())
                i=1
                
    writer.commit()
    
    writer = ix1.writer()
    
    for docname in os.listdir(dirCorreos):
        if not os.path.isdir(dirCorreos+docname):
            fileobj=open(dirCorreos+'\\'+docname,"rb")
            rte=unicode(fileobj.readline().strip())
            dtos=unicode(fileobj.readline().strip())
            fch=datetime.datetime.strptime(str(fileobj.readline().strip()),"%Y%m%d")
            ast=unicode(fileobj.readline().strip())
 #           print ast
            ctdo=unicode(fileobj.read())
            fileobj.close()
            writer.add_document(fichero=unicode(docname),remitente=rte,destinatario=dtos,fecha=fch,asunto=ast,cuerpo=ctdo)
            i+=1
            
        
    writer.commit()        
    tkMessageBox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " correos y "+str(j)+" contactos.")



    
def buscar(pattern):
    def listar(event):
        lista.delete(0,END)
        ixc=open_dir(dirindex1)
        ixa=open_dir(dirindex2)

        if pattern=="texto":
            with ixc.searcher() as searcher:
                query=MultifieldParser(["asunto","cuerpo"],ixc.schema).parse(unicode(entrada.get()))
                results= searcher.search(query)
                for r in results:
                    lista.insert(END,r['remitente'])
                    with ixa.searcher() as namesearch:
                        query=QueryParser('email',ixa.schema).parse(unicode(r['remitente']))
                        agenda=namesearch.search(query)
                        for name in agenda:
                            lista.insert(END,name['nombre'])
                    
                    lista.insert(END,'')
                    
        elif pattern=="spam":
            with ixc.searcher() as searcher:
                asuntos=entrada.get().strip().replace(" ", " OR ")        
                query=QueryParser("asunto",ixc.schema).parse(unicode(asuntos))
                results= searcher.search(query)
                for r in results:
                    lista.insert(END,r['fichero'])
                    lista.insert(END,'')
         

        elif pattern == "fecha":
            with ixc.searcher() as searcher:
                #Cogemos la fecha, la pasamos a datetime y como eso da error, la pasamos a solo date (no queremos time)
                biggerthan=datetime.datetime.strptime(entrada.get().strip(),"%Y%m%d").date()
                # {*fecha* to] <-- indica conjunto abierto hasta el final
                query=QueryParser("fecha",ixc.schema).parse(unicode("{"+str(biggerthan)+" to]"))
                results= searcher.search(query)
                for r in results:
                    lista.insert(END,r['remitente'])
                    lista.insert(END,r['destinatario'])
                    lista.insert(END,r['asunto'])
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
    menubar.add_command(label = "Indexar",command=index)
    bm= Menu(menubar,tearoff=0)
    bm.add_command(label = "Por texto", command= lambda: buscar("texto"))
    bm.add_command(label ="Por fecha",command= lambda: buscar("fecha"))
    bm.add_command(label="Spam",command= lambda: buscar("spam"))
    menubar.add_cascade(label="Buscar",menu=bm)
    top.config(menu=menubar)
    top.mainloop()
    

if __name__ == '__main__':
    principal()