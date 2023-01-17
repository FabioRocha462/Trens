#bibliotecas utilizadas
import time as t
import threading as th
from tkinter import *
from PIL import ImageTk, Image

#semáfors dos trens

#variável global para o start e o stop dos trens
START_TREM = True

#funções para o start e o stop
def stop():
    global START_TREM
    START_TREM = False
def start():
    global START_TREM
    START_TREM = True


#class trem
class Trem:
    #construtor inicial
    def __init__(self,coordenadaXI,coordenadaYI, canvas,timing,trem):
        self.coordenadaXI = coordenadaXI #x-inicial que corresponse o sentido horizontal
        self.coordenadaYI = coordenadaYI #y-inicial que corresponse o sentido vertical
        self.canvas = canvas #canvas para manipular as imagens e atualizar posições
        self.timing = timing #timing para controlar o tempo de cada trem irá movimentar-se
        self.trem = trem #imagem do trem criada com o canvas do app
        
        #colocando a imagem do trem na posição passadas como argumento
        TremEnv = self.canvas.create_image(
            self.coordenadaXI,
            self.coordenadaYI,
            image = self.trem,
            anchor = NW
        )
        
        self.imagem = TremEnv #agora passamos o tremEnv para a imagem criada


#função mover os trens            
def move(Trem,canvas): #recebemos o trem e o canvas (o trem para termos acesso as infirmações de imagem e o canvas para pegar a posiçao geral)
    global START_TREM # aqui tornamos o START_TREM como global
    coordx = float(Trem.coordenadaXI) #obtemos o coordenadaX do trem
    coordy = float(Trem.coordenadaYI) #obtemos o coordenadaY do trem
    #posições x e y para atualizar o move
    x = 0 
    y = 0

    # fazendo o laço de repetição entrar em loop
    while (START_TREM):
        coordenadas = canvas.coords(Trem.imagem) # obtendo as coordenadas do canvas
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
        
        canvas.move(Trem.imagem,x,y)#podemos mover os trens com a função do canvas chamada move passando estes três argumentos
        #fazemos o update
        root.update()
        #colocamos para dormir
        t.sleep(Trem.timing)

            
#class App
class App(object):
    #construtor
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

        TremInstance1 = Trem(135,430,self.canvas,float(self.TimeTrem1.get()),trem1)
        TremInstance2 = Trem(310,430,self.canvas,float(self.TimeTrem2.get()),trem2)
        TremInstance3 = Trem(485,430,self.canvas,float(self.TimeTrem3.get()),trem3)
        TremInstance4 = Trem(310,255,self.canvas,float(self.TimeTrem4.get()),trem4)   

        th.Thread(target=move,args=(TremInstance1,self.canvas)).start()
        th.Thread(target=move,args=(TremInstance2,self.canvas)).start()
        th.Thread(target=move,args=(TremInstance3,self.canvas)).start()
        th.Thread(target=move,args=(TremInstance4,self.canvas)).start()
                
                    


        

        
        

        
        
        


root = Tk()
app = App(root)
root.mainloop()






