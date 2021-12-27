class Auteur:
    # name -> son nom
    # ndoc -> nombre de documents publiés
    # production -> un dictionnaire des documents écrits par l'auteur
    
    def __init__(self, name, ndoc, productions):
        self.name = name
        self.ndoc = ndoc
        self.productions = productions
        
    def add(self, document):
        self.productions.append(document)
        
    def getAllDocuments(self):
        tousLesDocuments = []
        for production in self.productions:
            tousLesDocuments.append(production)
        return tousLesDocuments
    
    def tousDocuments(self):
        tousLesDocuments = ""
        for production in self.productions:
            tousLesDocuments += production.titre + " ; "
        return tousLesDocuments
        
    def __str__(self):
        return "L'auteur " + str(self.name) + " a écrit " + str(self.ndoc) + " document(s).\n" \
            + "Les titres sont les suivants : " + self.tousDocuments()