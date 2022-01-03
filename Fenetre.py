import tkinter as tk
from PIL import Image, ImageTk
from Corpus import Corpus
import networkx as nx
import matplotlib.pyplot as plt
from Graphe import Graphe

class Fenetre():
    # fenetre -> fenetre principale
    # collection -> tous les documents

    def __init__(self, collection):
        self.collection = collection
        Graphe(self.collection)
        self.fenetre = tk.Tk()
        # Agrandissement de la fenêtre au maximum
        self.fenetre.wm_state('zoomed')
        # Image contenant le graphe précedemment créé
        image = Image.open('./fig.png')
        self.hauteurImg = int(self.fenetre.winfo_screenheight()) - 120
        self.largeurImg = int((float(image.size[0]) * self.hauteurImg) / float(image.size[1]))
        image = image.resize((self.largeurImg, self.hauteurImg), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
         
        self.frameGraphe = tk.Frame(self.fenetre)
        self.frameGraphe.pack(side = tk.LEFT)
        self.labelFrame = tk.LabelFrame(self.frameGraphe, text="Graphe obtenu suite à l'analyse des textes", padx=20, pady=20)
        self.labelFrame.pack(fill="both", expand="yes")
        self.img = tk.Label(self.labelFrame, image=photo)
        self.img.pack()
        btn = tk.Button(self.fenetre, text='Update', command=self.testBouton)
        btn.pack()
        
        self.fenetre.mainloop()
        
    def testBouton(self):
        Graphe(self.collection)
        image = Image.open('./fig.png')
        image = image.resize((self.largeurImg, self.hauteurImg), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.img.configure(image=photo)
        self.img.image = photo
        self.fenetre.update()
        
        