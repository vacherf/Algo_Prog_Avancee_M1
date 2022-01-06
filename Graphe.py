import networkx as nx
import matplotlib.pyplot as plt
from stop_words import get_stop_words

class Graphe():
    # G -> graphe
    # docs -> documents
    # poidsMin -> poids mininum des arêtes à afficher
    
    def __init__(self, docs, poidsMin):
        self.G = nx.Graph()
        self.docs = docs
        self.poidsMin = poidsMin
        for doc in docs:
            # Traitement sur le texte
            texte = self.traiterTexte(doc)
            lgTexte = len(texte)
            if(lgTexte != 0):
                # Parcours du texte
                for i in range(lgTexte):
                    for j in range(i,lgTexte):
                        # Test pour éviter que deux noeuds aient le même nom
                        if(texte[i].lower() != texte[j].lower()):
                            # Teste l'existence d'une arête entre texte[i] et texte[j]
                            try:
                                # Incrémentation du poids de l'arête
                                self.G[texte[i].lower()][texte[j].lower()]['weight'] += 1 
                            except KeyError:     
                                # Création de l'arête
                                self.G.add_edge(texte[i].lower(), texte[j].lower(), weight=1)
                                
        # Suppression des arêtes ayant un poids inférieur au poids minimal saisi par l'utilisateur                          
        aretes = list(self.G.edges(data='weight'))
        for mot1,mot2,poids in aretes:
            if poids <= int(poidsMin):
                self.G.remove_edge(mot1, mot2)
        
        # Suppression des noauds n'ayant pas d'arêtes
        noeuds = list(self.G.nodes)
        for noeud in noeuds:
            if self.G.degree[noeud] < 1:
                self.G.remove_node(noeud)
                
        self.dessinerGraphe()
        
    def traiterTexte(self, texte):
        txt = texte
        caracSpe = ['.', '(', ')', ',', '\n']
        for carac in caracSpe:
            txt = txt.replace(carac, ' ')
        # Suppression des "stop-words"
        stop_words = get_stop_words('en')
        # Ajout de certains mots et caractères
        stop_words = stop_words + ['robotic', 'robotics', 'ie', 'also', 'e', '-', '!', '?']
        txtSplit = txt.split()
        txtClean = []
        # Parcours de la liste de mots
        for indice in range(len(txtSplit)):
            try:
                # Test si le mot est un "stopword" 
                stop_words.index(txtSplit[indice].lower()) 
            except ValueError:
                # Si le mot n'est pas un "stopword", on le met dans une liste "txtClean"
                txtClean.append(txtSplit[indice])
        return txtClean
        
    def rechercherMot(self, mot):
        if mot != "":
            aretes = list(self.G.edges(data='weight'))
            for mot1, mot2, poids in aretes:
                if mot1 != mot and mot2 != mot:
                    # Suppression des arêtes non liées au mot recherché par l'utilisateur
                    self.G.remove_edge(mot1, mot2)
                elif poids <= int(self.poidsMin):
                    self.G.remove_edge(mot1, mot2)
            noeuds = list(self.G.nodes)
            for noeud in noeuds:
                if self.G.degree[noeud] < 1:
                    # Suppression des noeuds inutiles
                    self.G.remove_node(noeud)   
        else:
            self.__init__(self.docs, self.poidsMin)
        self.dessinerGraphe()
        
    def dessinerGraphe(self):
        # Positionnement des noeuds en utilisant l'algorithme de Fruchterman-Reingold
        pos=nx.spring_layout(self.G)
        # Taille des noeuds en fonction de la taille du mot
        nx.draw(self.G,pos, node_size=[len(word) * 400 for word in self.G.nodes()], node_color='black')
        # Dictionnaire contenant les deux labels et le poids de l'arête entre u et v
        edge_labels=dict([((u,v,),d['weight'])
        for u,v,d in self.G.edges(data=True)])
        # Ecriture des poids
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels=edge_labels)
        # Ecriture des mots
        nx.draw_networkx_labels(self.G, pos, font_size=10, font_color='white')
        # Sauvegarde du graphe
        plt.savefig('fig.png', dpi=300)
    
            