import time as t
import threading as th
from tkinter import *
from PIL import ImageTk, Image


START_TREM = True
def stop():
    global START_TREM
    START_TREM = False
def start():
    global START_TREM
    START_TREM = True

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
    global START_TREM
    coordx = float(Trem.coordenadaXI)
    coordy = float(Trem.coordenadaYI)
    x = 0
    y = 0
    while (START_TREM):
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
        
        self.TimeTrem1 = Entry(app) 
        self.canvas.create_window(145,480, window=self.TimeTrem1)
        self.TimeTrem2 = Entry(app) 
        self.canvas.create_window(145,510, window=self.TimeTrem2)
        self.TimeTrem3 = Entry(app) 
        self.canvas.create_window(145,540, window=self.TimeTrem3)
        self.TimeTrem4 = Entry(app) 
        self.canvas.create_window(145,570, window=self.TimeTrem4)

        button = Button(text='Liberar',command=self.animation)
        self.canvas.create_window(145, 600, window=button)
        buttonStop = Button(text='Parar', command=stop)
        self.canvas.create_window(145, 630, window=buttonStop)
        buttonStart = Button(text='Continuar', command=start)
        self.canvas.create_window(200,630, window=buttonStart)

    def animation(self):
        global trem1
        global trem2
        global trem3
        global trem4

        trem1 = ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))
        trem2 =  ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))
        trem3 = ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))
        trem4 = ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))

        TremInstance1 = Trem(135,430,0,0,self.canvas,float(self.TimeTrem1.get()),trem1)
        TremInstance2 = Trem(310,430,0,0,self.canvas,float(self.TimeTrem2.get()),trem2)
        TremInstance3 = Trem(485,430,0,0,self.canvas,float(self.TimeTrem3.get()),trem3)
        TremInstance4 = Trem(310,250,0,0,self.canvas,float(self.TimeTrem4.get()),trem4)   

        th.Thread(target=move,args=(TremInstance1,self.canvas)).start()
        th.Thread(target=move,args=(TremInstance2,self.canvas)).start()
        th.Thread(target=move,args=(TremInstance3,self.canvas)).start()
        th.Thread(target=move,args=(TremInstance4,self.canvas)).start()
                
                    


        

        
        

        
        
        


root = Tk()
app = App(root)
root.mainloop()






