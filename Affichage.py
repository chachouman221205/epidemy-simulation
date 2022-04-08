from tkinter import *
from random import choice
from functools import partial
import regles

fen1 = Tk()
fen1.title('Simulation')
fen1.geometry('350x350')
can1 = Canvas(fen1,bg='white',height=300,width=300)
can1.pack()

case_libre = [e for e in range (0,100)]
L = []
l = []
coul = 'white'

for y in range (0,10):
    for x in range (0,10):
        can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = coul)
        l.append(coul)
    L.append(l)
    l = []

def Recommencer():
    L = []
    l = []
    coul = 'white'
    for y in range (0,10):
        for x in range (0,10):
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = coul)
            l.append(coul)
        L.append(l)
        l = []
    compteur.set(0)

def click(event):
    global compteur
    x = event.x//30
    y = event.y//30
    can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')
    compteur.set(compteur.get()+1)

def infect():
    global compteur
    l =  choice(case_libre)
    x = l%10
    y = (l-x)//10
    case_libre.remove(l)  
    can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')
    compteur.set(compteur.get()+1)
    
def nouvelle_regle():
    global R 
    regles.nouvelle_regle()
    R = regles.R
    
def Compteur():
    global compteur
    compteur = IntVar(value=0)
    Label(textvariable=compteur).pack()

couleurs = {"M":'black',"I":'red',"R":"grey","S":"white"}               

bou3 = Button(fen1,text='Infection',command=infect)
bou3.pack(side=RIGHT)

bou4 = Button(fen1,text='Paramètres',command=nouvelle_regle)
bou4.pack(side=RIGHT)

Compteur()

can1.bind("<Button-1>", click)

menubar = Menu(fen1)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=nouvelle_regle)
menu1.add_command(label="Editer", command=nouvelle_regle)
menu1.add_separator()
menu1.add_command(label="Quitter", command=quit)
menubar.add_cascade(label="Virus", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Réinitialiser", command=Recommencer)
menu2.add_command(label="Modifier", command=nouvelle_regle)
menubar.add_cascade(label="Affichage", menu=menu2)

fen1.config(menu=menubar)

mainloop()