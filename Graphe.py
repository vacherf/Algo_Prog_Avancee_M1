import networkx as nx
import matplotlib.pyplot as plt
from stop_words import get_stop_words

class Graphe():
    
    def __init__(self, docs):
        stop_words = get_stop_words('en')
        stop_words = stop_words + ['robotic', 'robotics']
        G = nx.Graph()
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
                                G[txtClean[i].lower()][txtClean[j].lower()]['weight'] += 1
                            except KeyError:     
                                G.add_edge(txtClean[i].lower(), txtClean[j].lower(), weight=1)
                                
        aretes = list(G.edges(data='weight'))
        for mot1,mot2,poids in aretes:
            if poids <= 30:
                G.remove_edge(mot1, mot2)
        noeuds = list(G.nodes)
        for noeud in noeuds:
            if G.degree[noeud] < 1:
                G.remove_node(noeud)       
        
        pos=nx.spring_layout(G)
        nx.draw(G,pos, node_size=[len(word) * 300 for word in G.nodes()], node_color='black')
        # specifiy edge labels explicitly
        edge_labels=dict([((u,v,),d['weight'])
        for u,v,d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
        nx.draw_networkx_labels(G, pos, font_size=10, font_color='white')
        # Sauvegarde du graphe
        
        plt.savefig('fig.png', dpi=300)
        plt.show(block=True)