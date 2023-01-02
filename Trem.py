import time as t
import threading as th
from tkinter import *
from PIL import ImageTk, Image



class Trem:
    def __init__(self,coordenadaXI,coordenadaYI,cooderdanaXF,coordernadaYF, canvas,timing,trem):
        self.coordenadaXI = coordenadaXI
        self.coordenadaYI = coordenadaYI
        self.cooderdanaXF = cooderdanaXF
        self.cooderdanaYF = coordernadaYF
        self.canvas = canvas
        self.timing = timing
        self.trem = trem
        
        TremEnv = self.canvas.create_image(
            self.coordenadaXI,
            self.coordenadaYI,
            image = self.trem,
            anchor = NW
        )
        
        self.imagem = TremEnv
                    
def move(Trem,canvas):
    coordx = float(Trem.coordenadaXI)
    coordy = float(Trem.coordenadaYI)
    x = 0
    y = 0
    while True:
        coordenadas = canvas.coords(Trem.imagem)
        if (coordenadas[0] == coordx) and (coordenadas[1] > coordy - 180):
            x = 0
            y = -5

        if (coordenadas[1] == coordy - 180) and (coordx + 175 > coordenadas[0]):
            y = 0
            x = 5

        if (coordenadas[0] == coordx + 175) and (coordy > coordenadas[1]):
            y = 5
            x= 0

        if (coordenadas[1] == coordy) and (coordx  < coordenadas[0]):
            y = 0
            x = -5

        canvas.move(Trem.imagem,x,y)
        root.update()
        t.sleep(Trem.timing)
                
                
                    
            

class App(object):
    def __init__(self, app, **kwargs):
        global background_image
        self.app = app
        self.canvas = Canvas(self.app,width=842,height=842)
        background_image = ImageTk.PhotoImage(Image.open('path.png').resize((526,351)))
        background = self.canvas.create_image(
            150,
            100,
            image = background_image,
            anchor = NW
        )
        
        self.canvas.pack()
        global trem1
        global trem2
        global trem3
        global trem4

        trem1 = ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))
        trem2 =  ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))
        trem3 = ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))
        trem4 = ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))
    
        TremInstance1 = Trem(135,430,0,0,self.canvas,0.1,trem1)
        TremInstance2 = Trem(310,430,0,0,self.canvas,0.5,trem2)
        TremInstance3 = Trem(485,430,0,0,self.canvas,0.2,trem3)
        TremInstance4 = Trem(310,250,0,0,self.canvas,0.3,trem4)
        th.Thread(target=move,args=(TremInstance1,self.canvas)).start()
        th.Thread(target=move,args=(TremInstance2,self.canvas)).start()
        th.Thread(target=move,args=(TremInstance3,self.canvas)).start()
        th.Thread(target=move,args=(TremInstance4,self.canvas)).start()

        
        
        


root = Tk()
app = App(root)
root.mainloop()






