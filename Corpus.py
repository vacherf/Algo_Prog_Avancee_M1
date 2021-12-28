import re
from datetime import datetime
# import pandas
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout 
from stop_words import get_stop_words

class Corpus:
    # nom -> le nom du corpus
    # authors -> le dictionnaire contenant les instances d'auteurs
    # id2aut -> le dictionnaire d'indice des auteurs
    # id2doc -> le dictionnaire d'indice des documents
    # ndoc -> comptage des docs
    # naut -> comptage des auteurs
    
    def __init__(self, nom, authors = {}, id2aut = {}, id2doc = {}):
        self.nom = nom
        self.authors = authors
        self.id2aut = id2aut
        self.id2doc = id2doc
        self.ndoc = len(id2doc)
        self.naut = len(id2aut)
        
    def afficherDocuments(self, nombre):
        tousDocuments = []
        nbTmp = nombre
        for key,auteur in self.authors.items():
            for document in auteur.getAllDocuments():    
                if nbTmp > 0:
                    tousDocuments.append(document)
                    nbTmp -= 1
                else:
                    break
        tousDocuments.sort(key=lambda x: datetime.strptime(x.date, '%d/%m/%Y'))
        return tousDocuments

# =============================================================================
#     def concorde(self, mot, texteGlobal, nbAvAp):
#         df = pandas.DataFrame(columns=["Contexte gauche", "Texte", "Contexte droit"])
#         searches = re.finditer(mot, texteGlobal)
#         index = 0
#         for search in searches:
#             df.loc[index] = ["..." + texteGlobal[search.start() - nbAvAp : search.start() + 1], mot, texteGlobal[search.end() : search.end() + nbAvAp] + "..."]
#             # df.append(texteGlobal[search.start() - 10 : search.start()], mot, texteGlobal[search.end() : search.end() + 10])
#             index += 1
#         print(df)
# =============================================================================
        
    def creationGraphe(self, docs):
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
# =============================================================================
#         pos = graphviz_layout(G, prog='dot')
#         edge_labels = nx.get_edge_attributes(G, 'label')
#         nx.draw(G, pos)
#         nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
#         nx.draw_networkx_labels(G, pos, font_size=10)
#         plt.show()
# =============================================================================
        aretes = list(G.edges(data='weight'))
        for mot1,mot2,poids in aretes:
            if poids <= 30:
                G.remove_edge(mot1, mot2)
        noeuds = list(G.nodes)
        for noeud in noeuds:
            if G.degree[noeud] < 1:
                G.remove_node(noeud)
        pos=nx.spring_layout(G)
        nx.draw(G,pos)
        # specifiy edge labels explicitly
        edge_labels=dict([((u,v,),d['weight'])
        for u,v,d in G.edges(data=True)])
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
        nx.draw_networkx_labels(G, pos, font_size=10)
        # show graphs
        plt.show()