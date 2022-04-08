from tkinter import *
from random import randint

fen1 = Tk()
fen1.title('Hello_World')
fen1.geometry('350x350')
can1 = Canvas(fen1,bg='white',height=300,width=300)
can1.pack()

L = []
l = []
coul = 'white'

for y in range (0,10):
    for x in range (0,10):
        can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = coul)
        l.append(coul)
    L.append(l)
    l = []
    
def key(event):
    print ("pressed")

def Save():
    L = []
    l = []
    coul = 'white'
    for y in range (0,10):
        for x in range (0,10):
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = coul)
            l.append(coul)
        L.append(l)
        l = []

def click(event):
    x = event.x//30
    y = event.y//30
    can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')

def infect():
    x = randint(0,9)
    y = randint(0,9)
    can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')
    
def Parametre():
    fen2 = Tk()
    fen2.title('Paramètres')
    fen2.geometry('250x250')
    #Texte de Nassim

couleurs = {"M":'black',"I":'red',"R":"grey","S":"white"}               

bou3 = Button(fen1,text='Infection',command=infect)
bou3.pack(side=RIGHT)

bou4 = Button(fen1,text='Paramètres',command=Parametre)
bou4.pack(side=RIGHT)

can1.bind("<Button-1>", click)

menubar = Menu(fen1)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=Parametre)
menu1.add_command(label="Editer", command=Parametre)
menu1.add_separator()
menu1.add_command(label="Quitter", command=quit)
menubar.add_cascade(label="Virus", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Réinitialiser", command=Save)
menu2.add_command(label="Modifier", command=Parametre)
menubar.add_cascade(label="Affichage", menu=menu2)

fen1.config(menu=menubar)

mainloop()