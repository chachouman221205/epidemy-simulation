from tkinter import *
from random import randint
fen1 = Tk()

can1 = Canvas(fen1,bg='white',height=300,width=300)
can1.pack()

def drawcadre():
    L = []
    l = []
    coul = 'white'
    for y in range (0,10):
        for x in range (0,10):
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = coul)
            l.append(coul)
        L.append(l)
        l = []
        
def infect():
    x = randint(0,10)
    y = randint(0,10)
    can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')

couleurs = {"M":'black',"I":'red',"R":"grey","S":"white"}
                
bou1 = Button(fen1,text='Quitter',command=fen1.quit)
bou1.pack()

bou2 = Button(fen1,text='Tracer une ligne',command=drawcadre)
bou2.pack(side=LEFT)

bou3 = Button(fen1,text='Infection',command=infect)
bou3.pack(side=RIGHT)
mainloop()