import tkinter as tk
from PIL import Image, ImageTk
from Corpus import Corpus
import networkx as nx
import matplotlib.pyplot as plt
from Graphe import Graphe
import pickle

class Fenetre():
    # fenetre -> fenetre principale
    # collection -> tous les documents
    # G -> graphe

    def __init__(self, collection):
        self.collection = collection
        self.poids = 30
        self.G = Graphe(self.collection, self.poids)
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
        
        self.frameAction = tk.Frame(self.fenetre)
        self.frameAction.pack()
        self.labelAction = tk.LabelFrame(self.frameAction, text="Rafraichissement du graphe en cas de bug", padx=20, pady=20)
        self.labelAction.pack(fill="both", expand="yes")
        btn = tk.Button(self.labelAction, text='Rafraichir', command=self.testBouton)
        btn.pack()
        
        self.labelMot = tk.LabelFrame(self.frameAction, text="Recherche de mot", padx=20, pady=20)
        self.labelMot.pack(fill="both", expand="yes")
        labelEntry = tk.Label(self.labelMot, text="Entrez un mot afin de centrer le graphe sur ce mot")
        labelEntry.pack()
        self.entree = tk.Entry(self.labelMot, width=30)
        self.entree.pack()
        bouton = tk.Button(self.labelMot, text="Rechercher", command=self.recherche)
        bouton.pack()
        
        self.labelPoids = tk.LabelFrame(self.frameAction, text="Selection du poids minimal", padx=20, pady=20)
        self.labelPoids.pack(fill="both", expand="yes")
        labelSpinbox1 = tk.Label(self.labelPoids, text="Veuillez choisir la valeur de poids minimal")
        labelSpinbox1.pack()
        labelSpinbox2 = tk.Label(self.labelPoids, text="(valeur par défaut : 30)")
        labelSpinbox2.pack()
        self.s = tk.Spinbox(self.labelPoids, from_=1, to=100)
        self.s.pack()
        tk.Button(self.labelPoids, text="Valider", command=self.poidsMinimal).pack()
        
        self.labelSave = tk.LabelFrame(self.frameAction, text="Sauvegarde/restauration", padx=20, pady=20)
        self.labelSave.pack(fill="both", expand="yes")
        print(self.frameAction.winfo_width())
        tk.Button(self.labelSave, text="Sauvegarder", command=self.sauvegarderGraphe, width=15).pack(side = tk.LEFT)
        tk.Button(self.labelSave, text="Restaurer", command=self.restaurerGraphe, width=15).pack(side = tk.RIGHT)

        self.fenetre.mainloop()
        
    def testBouton(self):
        self.G.dessinerGraphe()
        self.recharger_image()
    
    def recherche(self):
        self.G.rechercheMot(self.entree.get())
        self.recharger_image()
       
    def recharger_image(self):
        image = Image.open('./fig.png')
        image = image.resize((self.largeurImg, self.hauteurImg), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.img.configure(image=photo)
        self.img.image = photo
        self.fenetre.update()
      
    def poidsMinimal(self):
        self.poids = self.s.get()
        self.G = Graphe(self.collection, self.poids)
        self.recharger_image()
        
    def sauvegarderGraphe(self):
        with open("./graphe.pkl", "wb") as f:
            pickle.dump(self.G, f)
        
    def restaurerGraphe(self):
        with open("./graphe.pkl", "rb") as f:
            self.G = pickle.load(f)
        self.G.dessinerGraphe()
        self.recharger_image()
        