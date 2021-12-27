import datetime

# from gensim.summarization import summarize

class Document:
    # titre -> titre du document
    # auteur -> le nom de l'auteur
    # date -> la date de publication
    # url -> url source
    # texte -> le contenu textuel du document
    
    def __init__(self, titre, date=datetime.datetime.today().year, url="", texte="", type=""):
        self.titre = titre
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type
    
    def __str__(self):
        return "Le document s'intitule " + self.titre \
            + ", écrit le " + self.date \
            + ", accessible à l'url suivant : " + self.url + ".\n" \
            + "Le document contient le texte suivant : \n" + self.texte
            
    def __repr__(self):
        return "Titre : " + self.titre + "\n" \
                "Date : " + self.date + "\n" \
                "URL : " + self.url + "\n" \
                "Texte : " + self.texte + "\n"

    # def resume(self):
    #     return gensim.summarize(self.texte)
                
class RedditDocument(Document):
    # auteur -> auteur de l'article
    # nbComm -> nombre de commentaires de l'article Reddit
    
    def __init__(self, titre, date, url, texte, auteur, nbComm):
        super().__init__(titre, date, url, texte)
        self.auteur = auteur
        self.__nbComm = nbComm
    
    def getNbComm(self):
        return self.nbComm

    def getType(self):
        return "Reddit"
    
    def __str__(self):
        return super().__str__() + \
            "L'auteur est " + self.auteur + ".\n" \
            "Il y a " + self.nbComm + " commentaire(s). \n"

    def __repr__(self):
        return super().__repr__() + \
            "Auteur : " + str(self.auteur) + "\n" \
            "Nb commentaires : " + str(self.__nbComm) + "\n"
            
class ArxivDocument(Document):
    # coAuteur -> liste de tous les auteurs
    
    def __init__(self, titre, date, url, texte, coAuteur=[]):
        super().__init__(titre, date, url, texte)
        self.coAuteur = coAuteur
        
    def addCoAuteur(self, auteur):
        self.coAuteur.append(auteur)
    
    def tousAuteurs(self):
        tousLesAuteurs = ""
        for i in range(len(self.coAuteur)):
            tousLesAuteurs += self.coAuteur[i]['name']
            if i != len(self.coAuteur) - 1:
                tousLesAuteurs += ", "
        return tousLesAuteurs

    def getType(self):
        return "Arxiv"
        
    def __str__(self):
        return super().__str__() + \
            "Les co-auteurs sont " + self.tousAuteurs() + "\n"

    def __repr__(self):
        return super().__repr__() + \
            "Auteurs : " + self.tousAuteurs() + "\n"