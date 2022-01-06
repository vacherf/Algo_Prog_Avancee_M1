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
                for i in range(lgTexte):
                    for j in range(i,lgTexte):
                        if(texte[i].lower() != texte[j].lower()):
                            try:
                                self.G[texte[i].lower()][texte[j].lower()]['weight'] += 1
                            except KeyError:     
                                self.G.add_edge(texte[i].lower(), texte[j].lower(), weight=1)
                                
        aretes = list(self.G.edges(data='weight'))
        for mot1,mot2,poids in aretes:
            if poids <= int(poidsMin):
                self.G.remove_edge(mot1, mot2)
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
        for indice in range(len(txtSplit)):
            try:
                stop_words.index(txtSplit[indice].lower())
            except ValueError:
                txtClean.append(txtSplit[indice])
        return txtClean
        
    def rechercherMot(self, mot):
        if mot != "":
            aretes = list(self.G.edges(data='weight'))
            for mot1, mot2, poids in aretes:
                if mot1 != mot and mot2 != mot:
                    # Suppression des arêtes inutiles
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
        pos=nx.spring_layout(self.G)
        # Taille des noeuds en fonction de la taille du mot
        nx.draw(self.G,pos, node_size=[len(word) * 400 for word in self.G.nodes()], node_color='black')
        
        edge_labels=dict([((u,v,),d['weight'])
        for u,v,d in self.G.edges(data=True)])
        # Ecriture des poids
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels=edge_labels)
        # Ecriture des mots
        nx.draw_networkx_labels(self.G, pos, font_size=10, font_color='white')
        # Sauvegarde du graphe
        plt.savefig('fig.png', dpi=300)
        plt.show(block=True)
        
    
            