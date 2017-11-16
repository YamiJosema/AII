from Tkinter import Menu
import Tkinter
import tkMessageBox

from whoosh.fields import *
from whoosh.index import *
from whoosh.qparser import *


dirindex1 = "Index/Agenda"
dirindex2= "Index/Correos"
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
            fch=unicode(fileobj.readline().strip())
            ast=unicode(fileobj.readline().strip())
            ctdo=unicode(fileobj.read())
            fileobj.close()
            writer.add_document(fichero=unicode(docname),remitente=rte,destinatario=dtos,fecha=fch,asunto=ast,cuerpo=ctdo)
            i+=1
            
        
    writer.commit()        
    tkMessageBox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " correos y "+str(j)+" contactos.")

    
def fecha():
    print "hello"

    
def texto():
    print "hello"

    
def spam():
    print "hello"

    


def principal():
    top = Tkinter.Tk()
    menubar = Menu(top)
    menubar.add_command(label = "Indexar",command= index)
    bm= Menu(menubar,tearoff=0)
    bm.add_command(label = "Por texto", command = texto)
    bm.add_command(label ="Por fecha", command = fecha)
    bm.add_command(label="Spam",command=spam)
    menubar.add_cascade(label="Buscar",menu=bm)
    top.config(menu=menubar)
    top.mainloop()
    

if __name__ == '__main__':
    principal()