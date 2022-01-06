from Documents import RedditDocuments
from Documents import ArxivDocuments
import tkinter as tk
from PIL import Image, ImageTk
from Graphe import Graphe
import pickle
from tkinter.filedialog import askopenfilename, asksaveasfilename


class Application():
    # fenetre -> fenetre principale
    # collection -> tous les documents
    # G -> graphe
    # nbDocReddit -> nombre de documents venant de Reddit à traiter
    # nbDocArxiv -> nombre de documents venant de Arxiv à traiter

    def __init__(self):
        self.nbDocReddit = 5
        self.nbDocArxiv = 5
        self.reddit = RedditDocuments(self.nbDocReddit)
        self.arxiv = ArxivDocuments(self.nbDocArxiv)
        self.collection = self.reddit.documents + self.arxiv.documents
        # Poids minimal par défaut
        self.poids = 30
        self.G = Graphe(self.collection, self.poids)
        self.fenetre = tk.Tk()
        # Agrandissement de la fenêtre au maximum
        self.fenetre.wm_state('zoomed')
        # Affichage du graphe obtenu
        self.affichageGraphe()
        # Affichage des évenements permettant d'intéragir avec le graphe
        self.actionGraphe()
        # Lancement de la fenêtre principale
        self.fenetre.mainloop()

    def affichageGraphe(self):
        frameGraphe = tk.Frame(self.fenetre)
        frameGraphe.pack(side=tk.LEFT)
        labelFrame = tk.LabelFrame(frameGraphe, text="Graphe obtenu suite à l'analyse des textes", padx=20, pady=20)
        labelFrame.pack(fill="both", expand="yes")
        self.img = tk.Label(labelFrame)
        self.img.pack()
        self.chargerImage()

    def actionGraphe(self):
        frameAction = tk.Frame(self.fenetre)
        frameAction.pack()
        labelAction = tk.LabelFrame(frameAction, text="Rafraichissement du graphe en cas de bug d'affichage (superposition des noeuds)", padx=20, pady=20)
        labelAction.pack(fill="both", expand="yes")
        btn = tk.Button(labelAction, text='Rafraichir', command=self.rafraichir)
        btn.pack()

        labelChoix = tk.LabelFrame(frameAction, text="Choix du nombre de documents", padx=20, pady=20)
        labelChoix.pack(fill="both", expand="yes")
        tk.Label(labelChoix, text="Entrez le nombre de documents Reddit souhaités").pack()
        redditDefaut = tk.StringVar(self.fenetre)
        redditDefaut.set(self.nbDocReddit)
        self.docreddit = tk.Spinbox(labelChoix, from_=0, to=30, textvariable=redditDefaut)
        self.docreddit.pack()
        tk.Label(labelChoix, text="Entrez le nombre de documents Arxiv souhaités").pack()
        arxivDefaut = tk.StringVar(self.fenetre)
        arxivDefaut.set(self.nbDocArxiv)
        self.docarxiv = tk.Spinbox(labelChoix, from_=0, to=30, textvariable=arxivDefaut)
        self.docarxiv.pack()
        bouton = tk.Button(labelChoix, text="Valider", command=self.choixNombreDocuments)
        bouton.pack()

        labelMot = tk.LabelFrame(frameAction, text="Recherche de mot", padx=20, pady=20)
        labelMot.pack(fill="both", expand="yes")
        labelEntry = tk.Label(labelMot, text="Entrez un mot afin de centrer le graphe sur ce mot")
        labelEntry.pack()
        self.rechercheMot = tk.Entry(labelMot, width=30)
        self.rechercheMot.pack()
        tk.Button(labelMot, text="Rechercher", command=self.recherche).pack()

        labelPoids = tk.LabelFrame(frameAction, text="Selection du poids minimal", padx=20, pady=20)
        labelPoids.pack(fill="both", expand="yes")
        tk.Label(labelPoids, text="Veuillez choisir la valeur de poids minimal").pack()
        poidsDefaut = tk.StringVar(self.fenetre)
        poidsDefaut.set(self.poids)
        self.poidsSx = tk.Spinbox(labelPoids, from_=1, to=100, textvariable=poidsDefaut)
        self.poidsSx.pack()
        tk.Button(labelPoids, text="Valider", command=self.poidsMinimal).pack()

        labelSave = tk.LabelFrame(frameAction, text="Sauvegarde/restauration", padx=20, pady=20)
        labelSave.pack(fill="both", expand="yes")
        tk.Button(labelSave, text="Sauvegarder", command=self.sauvegarderGraphe, width=15).pack(side=tk.LEFT)
        tk.Button(labelSave, text="Restaurer", command=self.restaurerGraphe, width=15).pack(side=tk.RIGHT)
        
    def rafraichir(self):
        self.G.dessinerGraphe()
        self.chargerImage()

    def choixNombreDocuments(self):
        self.reddit = RedditDocuments(int(self.docreddit.get()))
        self.arxiv = ArxivDocuments(int(self.docarxiv.get()))
        self.collection = self.reddit.documents + self.arxiv.documents
        self.G = Graphe(self.collection, self.poids)
        self.chargerImage()
    
    def recherche(self):
        self.G.rechercherMot(self.rechercheMot.get())
        self.chargerImage()
       
    def chargerImage(self):
        # Image contenant le graphe précedemment créé
        image = Image.open('./fig.png')
        # Hauteur de l'image en fonction de la taille de l'écran
        self.hauteurImg = int(self.fenetre.winfo_screenheight()) - 100
        # Largeur de l'image en fonction de la hauteur de l'image afin d'éviter une déformation de celle-ci
        self.largeurImg = int((float(image.size[0]) * self.hauteurImg) / float(image.size[1]))
        image = image.resize((self.largeurImg, self.hauteurImg), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.img.configure(image=photo)
        self.img.image = photo
        self.fenetre.update()
      
    def poidsMinimal(self):
        self.poids = self.poidsSx.get()
        self.G = Graphe(self.collection, self.poids)
        self.chargerImage()
        
    def sauvegarderGraphe(self):
        filepath = asksaveasfilename(title="Sauvegarder", filetypes=[('pickle files', '.pkl'), ('all files', '.*')])
        with open(filepath + ".pkl", "wb") as f:
            pickle.dump(self.G, f)
        
    def restaurerGraphe(self):
        filepath = askopenfilename(title="Charger une sauvegarde", filetypes=[('pickle files', '.pkl'), ('all files', '.*')])
        with open(filepath, "rb") as f:
            self.G = pickle.load(f)
        self.G.dessinerGraphe()
        self.chargerImage()
        