from Tkinter import Menu
import Tkinter

def index():
    print "nada"
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