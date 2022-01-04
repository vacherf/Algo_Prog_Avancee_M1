# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 11:31:46 2022

@author: rpons
"""

from tkinter import *    
fenetre = Tk()
label = Label(fenetre, text="Hello World")
label.pack()
def recup_valeurs():
    global mot 
    mot = entree.get()  
    global valeur
    valeur=s.get()
entree = Entry(fenetre, width=30)
entree.pack()
s = Spinbox(fenetre, from_=1, to=100)
s.pack()
bouton=Button(fenetre, text="Valider", command=recup_valeurs)
bouton.pack()
fenetre.mainloop()
print(mot)
print(valeur)