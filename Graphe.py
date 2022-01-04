import networkx as nx
import matplotlib.pyplot as plt
from stop_words import get_stop_words
import pickle

class Graphe():
    # G -> graphe
    # docs -> documents
    # poidsMin -> poids mininum des arêtes à afficher
    
    def __init__(self, docs, poidsMin):
        stop_words = get_stop_words('en')
        stop_words = stop_words + ['robotic', 'robotics']
        self.G = nx.Graph()
        self.docs = docs
        self.poidsMin = poidsMin
        for doc in docs:
            # Suppression des points dans le texte
            txt = doc.texte.replace(".","")
            txtSplit = txt.split()
            txtClean = []
            for indice in range(len(txtSplit)):
                try:
                    ind = stop_words.index(txtSplit[indice].lower())
                except ValueError:
                    ind = -1
                # Suppression des "stop-words"
                if(ind == -1):
                    txtClean.append(txtSplit[indice])
            if(len(txtClean) != 0):
                for i in range(len(txtClean)):
                    for j in range(i,len(txtClean)):
                        if(txtClean[i].lower() != txtClean[j].lower()):
                            try:
                                self.G[txtClean[i].lower()][txtClean[j].lower()]['weight'] += 1
                            except KeyError:     
                                self.G.add_edge(txtClean[i].lower(), txtClean[j].lower(), weight=1)
                                
        aretes = list(self.G.edges(data='weight'))
        for mot1,mot2,poids in aretes:
            if poids <= int(poidsMin):
                self.G.remove_edge(mot1, mot2)
        noeuds = list(self.G.nodes)
        for noeud in noeuds:
            if self.G.degree[noeud] < 1:
                self.G.remove_node(noeud)  
        print(self.G)
        self.dessinerGraphe()
        
    def rechercheMot(self, mot):
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
        nx.draw(self.G,pos, node_size=[len(word) * 300 for word in self.G.nodes()], node_color='black')
        
        edge_labels=dict([((u,v,),d['weight'])
        for u,v,d in self.G.edges(data=True)])
        # Ecriture des poids
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels=edge_labels)
        # Ecriture des mots
        nx.draw_networkx_labels(self.G, pos, font_size=10, font_color='white')
        # Sauvegarde du graphe
        plt.savefig('fig.png', dpi=300)
        plt.show(block=True)
        
    
            