#bibliotecas utilizadas
import time as t
import threading as th
from tkinter import *
from PIL import ImageTk, Image

#semáfors dos trens
semaforo12 = th.Semaphore(4)
semaforo21 = th.Semaphore(4)
semaforo14 = th.Semaphore(4)
semaforo24 = th.Semaphore(4)
semaforo32 = th.Semaphore(4)
semaforo23 = th.Semaphore(4)
semaforo42 = th.Semaphore(4)
semaforo43 = th.Semaphore(4)
semaforo2 = th.Semaphore(4)
semaforo3 = th.Semaphore(4)
semaforo4 = th.Semaphore(4)

dict = {}
#variável global para o start e o stop dos trens
START_TREM = True

#funções para o start e o stop
def stop():
    global START_TREM
    START_TREM = False
def start():
    global START_TREM
    START_TREM = True


#variáveis globais para informar aos semáforos onde estão os trens
#trem 1
positionx1 = 0
positiony1 = 0

#trem 2
positionx2 = 0
positiony2 = 0

#trem 3
positionx3 = 0
positiony3 = 0

#trem 4
positionx4 = 0
positiony4 = 0



#class trem
class Trem:
    #construtor inicial
    def __init__(self,coordenadaXI,coordenadaYI, canvas,timing,trem,name):
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
        self.name = name
        
    def get_name(self):
        return self.name


#função mover os trens            
def move(Trem,canvas): #recebemos o trem e o canvas (o trem para termos acesso as infirmações de imagem e o canvas para pegar a posiçao geral)
    global START_TREM # aqui tornamos o START_TREM como global
    global positionx1,positiony1,positionx4,positiony4,positionx2,positiony2,positionx3,positiony3
    coordx = float(Trem.coordenadaXI) #obtemos o coordenadaX do trem
    coordy = float(Trem.coordenadaYI) #obtemos o coordenadaY do trem
    #velocidade dos trens
    global velocidade1,velocidade2,velocidade3,velocidade4
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

        if (Trem.get_name() == "trem1"):
            velocidade1 = Trem.timing
            positionx1,positiony1 = coordenadas[0],coordenadas[1]
            if (positionx1 > 135 and positiony1 == 250) and (positionx2 == 310 and positiony2 < 430):
                    semaforo12.acquire()

            if (positionx1 > 135 and positiony1 == 250) and (positionx4 < 485 and positiony4 == 255): 
                semaforo14.acquire()

            if(positionx1 < 280 and positiony1 == 430) and (positionx2 < 470 and positiony2 == 430):
                semaforo21.release()

        if (Trem.get_name() == "trem2"):
            # relaçao entre trem 2 e trem 4
            positionx2,positiony2 = coordenadas[0],coordenadas[1]
            velocidade2 = Trem.timing
            if (positiony2 == 250 and positionx2 > 320) and (positionx1 > 135 and positiony1 == 250):
                    semaforo12.release()
            if(positionx2 == 310 and positiony2 < 350 ) and (positionx4 < 485 and positiony4 == 255):
                semaforo24.acquire()

            if(positionx4 == 485 and positiony4 > 90)  and (positionx2 == 485 and positiony2 > 250):
                semaforo42.release()
            
            #relaçao entre 2 e 1

            if (positionx2 < 485 and positiony2 == 430) and (positionx1 == 310 and positiony1 > 250):

                semaforo21.acquire()
            #relaçao entre 2 e 3

            if(positionx2 > 310 and positiony2 == 430) and (positionx3 < 660 and positiony3 == 430):
                semaforo32.release()

            if (positiony2 == 250 and positionx2 >310) and (positionx3 == 485 and positiony3 > 250):
                semaforo23.acquire()


        if (Trem.get_name() == "trem3"):
            #relaçao entre 3 e 2
            positionx3,positiony3 = coordenadas[0],coordenadas[1]
            #relação entre trem 3 e 2
            velocidade3 = Trem.timing
            if (positionx3 < 670 and positiony3 == 430) and (positionx2 > 310 and positiony2 == 250):
                semaforo32.acquire()
            
             #RELAÇÃO ENTRE 4 E 3

            if(positionx4 == 485 and positiony4 > 200) and (positionx3 > 500 and positiony3 == 250):
                semaforo43.release()

            #relação entre 2 e 3

            if (positionx3 > 500 and positiony3 == 250) and (positionx2 >310 and positiony2 == 250 ):
                semaforo23.release()

        if (Trem.get_name() == "trem4"):
            positionx4,positiony4 = coordenadas[0],coordenadas[1]
            velocidade4 = Trem.timing
            #relação entre  1 e 4
            if (positiony4 > 200 and positionx4 == 310) and (positionx1 > 150 and positiony1 == 250):
                semaforo14.release()
            #RELAÇÃO ENTRE 4 E 2
            if (positiony4 > 200 and positionx4 == 310) and (positionx2 == 310 and positiony2 < 350 ) :
                semaforo24.release()
            if (positionx4 == 485 and positiony4 > 90) and (positionx2 > 310 and positiony2 == 250):
                semaforo42.acquire()
            #RELAÇÃO ENTRE 4 E 3
            if(positionx4 == 485 and positiony4 > 200) and (positionx3 == 485 and positiony3 < 430):
                semaforo43.acquire()


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
        global ImageSemaforo1
        global ImageSemaforo2
        global ImageSemaforo3
        global ImageSemaforo4
        self.app = app
        self.canvas = Canvas(self.app,width=842,height=842)
        background_image = ImageTk.PhotoImage(Image.open('path.png').resize((526,351)))
        background = self.canvas.create_image(
            150,
            100,
            image = background_image,
            anchor = NW
        )
        ImageSemaforo1 = ImageTk.PhotoImage(Image.open('semaforo-png.png').resize((20,20)))
        SemaforoCanvas1 = self.canvas.create_image(
            315,
            265,
            image = ImageSemaforo1,
            anchor = NW

        )
        SemaforoCanvas2 = self.canvas.create_image(
            315,
            440,
            image = ImageSemaforo1,
            anchor = NW

        )

        SemaforoCanvas3 = self.canvas.create_image(
            490,
            440,
            image = ImageSemaforo1,
            anchor = NW

        )
    
        SemaforoCanvas4 = self.canvas.create_image(
            490,
            265,
            image = ImageSemaforo1,
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
        global dict
        trem1 = ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))
        trem2 =  ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))
        trem3 = ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))
        trem4 = ImageTk.PhotoImage(Image.open('trem.png').resize((30,30)))

        TremInstance1 = Trem(135,430,self.canvas,float(self.TimeTrem1.get()),trem1,"trem1")
        TremInstance2 = Trem(310,430,self.canvas,float(self.TimeTrem2.get()),trem2,"trem2")
        TremInstance3 = Trem(485,430,self.canvas,float(self.TimeTrem3.get()),trem3,"trem3")
        TremInstance4 = Trem(310,255,self.canvas,float(self.TimeTrem4.get()),trem4,"trem4")   

        thread1 = th.Thread(target=move,args=(TremInstance1,self.canvas)).start()
        dict[TremInstance1] = th.get_native_id()
        thread2 = th.Thread(target=move,args=(TremInstance2,self.canvas)).start()
        dict[TremInstance2] = th.get_native_id()
        thread3 = th.Thread(target=move,args=(TremInstance3,self.canvas)).start()
        dict[TremInstance3] = th.get_native_id()
        thread4 = th.Thread(target=move,args=(TremInstance4,self.canvas)).start()
        dict[TremInstance4] = th.get_native_id()

        

                
                    


        

        
        

        
        
        


root = Tk()
app = App(root)

root.mainloop()






