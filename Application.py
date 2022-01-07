from Documents import RedditDocuments
from Documents import ArxivDocuments
import tkinter as tk
from PIL import Image, ImageTk
from Graphe import Graphe
import pickle
from tkinter.filedialog import askopenfilename, asksaveasfilename


class Application():
    # nbDocReddit -> nombre de documents venant de Reddit à traiter
    # nbDocArxiv -> nombre de documents venant de Arxiv à traiter
    # poids -> poids minimal des arêtes à afficher
    # collection -> tous les documents Reddit et Arxiv réunis
    # G -> graphe
    # fenetre -> fenetre principale
    # img -> label contenant l'image du graphe
    # docReddit -> spinbox permettant le choix du nombre de documents Reddit
    # docArxiv -> spinbox permettant le choix du nombre de documents Arxiv
    # rechercheMot -> zone de texte afin d'entrer un mot à chercher
    # poidsSx -> spinbox permettant le choix du poids minimal à afficher

    def __init__(self):
        # Initialisation du nombre de documents à 5 pour les deux sources de données
        self.nbDocReddit = 5
        self.nbDocArxiv = 5
        reddit = RedditDocuments(self.nbDocReddit)
        arxiv = ArxivDocuments(self.nbDocArxiv)
        self.collection = reddit.documents + arxiv.documents
        # Poids minimal par défaut
        self.poids = 30
        self.G = Graphe(self.collection, self.poids)
        self.fenetre = tk.Tk()
        self.fenetre.title("Projet algorithmique et programmation avancée - PONSON - VACHER")
        # Agrandissement de la fenêtre au maximum
        self.fenetre.wm_state('zoomed')
        # Affichage du graphe obtenu
        self.affichageGraphe()
        # Affichage des évenements permettant d'intéragir avec le graphe
        self.actionGraphe()
        # Lancement de la fenêtre principale
        self.fenetre.mainloop()

    def affichageGraphe(self):
        # Création d'une frame qui va contenir le graphe à gauche de la fenêtre
        frameGraphe = tk.Frame(self.fenetre)
        frameGraphe.pack(side=tk.LEFT)
        # Titre au dessus du graphe
        labelFrame = tk.LabelFrame(frameGraphe, text="Graphe obtenu suite à l'analyse des textes", padx=20, pady=20)
        labelFrame.pack(fill="both", expand="yes")
        # label contenant l'image du graphe
        self.img = tk.Label(labelFrame)
        self.img.pack()
        self.chargerImage()

    def actionGraphe(self):
        # Création d'une frame qui va contenir les actions (à droite de la fenêtre)
        frameAction = tk.Frame(self.fenetre)
        frameAction.pack()
        # Gestion du rafraichissement en cas de bug d'affichage
        labelAction = tk.LabelFrame(frameAction, text="Rafraichissement du graphe en cas de bug d'affichage (superposition des noeuds)", padx=20, pady=20)
        labelAction.pack(fill="both", expand="yes")
        btn = tk.Button(labelAction, text='Rafraichir', command=self.rafraichir)
        btn.pack()
        
        # Gestion du nombre de documents
        labelChoix = tk.LabelFrame(frameAction, text="Choix du nombre de documents", padx=20, pady=20)
        labelChoix.pack(fill="both", expand="yes")
        tk.Label(labelChoix, text="Entrez le nombre de documents Reddit souhaités").pack()
        # Valeur par défaut que va contenir le spinbox
        redditDefaut = tk.StringVar(self.fenetre)
        redditDefaut.set(self.nbDocReddit)
        # Création du spinbox permettant le chox du nombre de documents souhaités
        self.docReddit = tk.Spinbox(labelChoix, from_=0, to=30, textvariable=redditDefaut)
        self.docReddit.pack()
        tk.Label(labelChoix, text="Entrez le nombre de documents Arxiv souhaités").pack()
        arxivDefaut = tk.StringVar(self.fenetre)
        arxivDefaut.set(self.nbDocArxiv)
        self.docArxiv = tk.Spinbox(labelChoix, from_=0, to=30, textvariable=arxivDefaut)
        self.docArxiv.pack()
        bouton = tk.Button(labelChoix, text="Valider", command=self.choixNombreDocuments)
        bouton.pack()
        
        # Gestion de la recherche du mot à centrer
        labelMot = tk.LabelFrame(frameAction, text="Recherche du mot à centrer", padx=20, pady=20)
        labelMot.pack(fill="both", expand="yes")
        labelEntry = tk.Label(labelMot, text="Entrez un mot afin de centrer le graphe sur ce mot")
        labelEntry.pack()
        # Création d'une zone de texte
        self.rechercheMot = tk.Entry(labelMot, width=30)
        self.rechercheMot.pack()
        tk.Button(labelMot, text="Rechercher", command=self.recherche).pack()

        # Gestion du poids minimal à afficher
        labelPoids = tk.LabelFrame(frameAction, text="Selection du poids minimal", padx=20, pady=20)
        labelPoids.pack(fill="both", expand="yes")
        tk.Label(labelPoids, text="Veuillez choisir la valeur de poids minimal").pack()
        poidsDefaut = tk.StringVar(self.fenetre)
        poidsDefaut.set(self.poids)
        self.poidsSx = tk.Spinbox(labelPoids, from_=1, to=100, textvariable=poidsDefaut)
        self.poidsSx.pack()
        tk.Button(labelPoids, text="Valider", command=self.poidsMinimal).pack()
        
        # Gestion de la sauvergarde et de l'importation
        labelSave = tk.LabelFrame(frameAction, text="Sauvegarde/importation", padx=20, pady=20)
        labelSave.pack(fill="both", expand="yes")
        tk.Button(labelSave, text="Sauvegarder", command=self.sauvegarderGraphe, width=15).pack(side=tk.LEFT)
        tk.Button(labelSave, text="Importer", command=self.restaurerGraphe, width=15).pack(side=tk.RIGHT)
        
    def rafraichir(self):
        self.G.dessinerGraphe()
        self.chargerImage()

    def choixNombreDocuments(self):
        # Création d'une nouvelle collection en fonction des valeurs saisies par l'utilisateur
        reddit = RedditDocuments(int(self.docReddit.get()))
        arxiv = ArxivDocuments(int(self.docArxiv.get()))
        self.collection = reddit.documents + arxiv.documents
        self.G = Graphe(self.collection, self.poids)
        self.chargerImage()
    
    def recherche(self):
        self.G.rechercherMot(self.rechercheMot.get())
        self.chargerImage()
       
    def chargerImage(self):
        # Image contenant le graphe précedemment créé
        image = Image.open('./fig.png')
        # Hauteur de l'image en fonction de la taille de l'écran
        hauteurImg = int(self.fenetre.winfo_screenheight()) - 100
        # Largeur de l'image en fonction de la hauteur de l'image afin d'éviter une déformation de celle-ci
        largeurImg = int((float(image.size[0]) * hauteurImg) / float(image.size[1]))
        image = image.resize((largeurImg, hauteurImg), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        # Implantation de l'image dans le label
        self.img.configure(image=photo)
        self.img.image = photo
        self.fenetre.update()
      
    def poidsMinimal(self):
        # Création d'un nouveau graphe avec le poids minimal saisi par l'utilisateur
        self.poids = self.poidsSx.get()
        self.G = Graphe(self.collection, self.poids)
        self.chargerImage()
        
    def sauvegarderGraphe(self):
        # Ouverture d'une fenêtre permettant de choisir l'emplacement et le nom du fichier de sauvergarde
        filepath = asksaveasfilename(title="Sauvegarder", filetypes=[('pickle files', '.pkl'), ('all files', '.*')])
        # Enregistrement du graphe courant dans un fichier .pkl
        with open(filepath + ".pkl", "wb") as f:
            pickle.dump(self.G, f)
        
    def restaurerGraphe(self):
        # Ouverture d'une fenêtre permettant de choisir le fichier de sauvegarde à importer
        filepath = askopenfilename(title="Charger une sauvegarde", filetypes=[('pickle files', '.pkl'), ('all files', '.*')])
        # Lecture du fichier
        with open(filepath, "rb") as f:
            self.G = pickle.load(f)
        self.G.dessinerGraphe()
        self.chargerImage()
        