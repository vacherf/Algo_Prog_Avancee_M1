import re
from datetime import datetime
import pandas

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

    def concorde(self, mot, texteGlobal, nbAvAp):
        df = pandas.DataFrame(columns=["Contexte gauche", "Texte", "Contexte droit"])
        searches = re.finditer(mot, texteGlobal)
        index = 0
        for search in searches:
            df.loc[index] = ["..." + texteGlobal[search.start() - nbAvAp : search.start() + 1], mot, texteGlobal[search.end() : search.end() + nbAvAp] + "..."]
            # df.append(texteGlobal[search.start() - 10 : search.start()], mot, texteGlobal[search.end() : search.end() + 10])
            index += 1
        print(df)