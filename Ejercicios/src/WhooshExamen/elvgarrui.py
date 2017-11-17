from Tkinter import Menu
import Tkinter
import tkMessageBox

from bs4 import BeautifulSoup
import requests


def index():
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
                texto+=p.get_text()+" "
            
                
        if int(i)==4:
            break
    
#insert     
#    cursor = conn.execute("SELECT COUNT(*) FROM CRONICAS")

     

    tkMessageBox.showinfo( "Informacion"+ " cronicas y " +" goles.")
 
    
    
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
    bm.add_command(label = "Noticia", command= lambda: buscar("noticia"))
    bm.add_command(label ="Fecha",command= lambda: buscar("fecha"))
    bm.add_command(label="Autor",command= lambda: buscar("autor"))
    menubar.add_cascade(label="Buscar",menu=bm)
    top.config(menu=menubar)
    top.mainloop()
    

if __name__ == '__main__':
    principal()