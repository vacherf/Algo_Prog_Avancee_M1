import praw
import urllib.request
import xmltodict

class Documents():
    # theme -> thème de tous les documents récupérés
    # documents -> tous les documents récupérés
    
    def __init__(self):
        self.theme = 'robotics'
        self.documents = []
        
class RedditDocuments(Documents):
    # nbDocuments -> nombre de documents Reddit à récupérer
    
    def __init__(self, nbDocuments):
        super().__init__()
        self.nbDocuments = nbDocuments
        self.connexion()
        self.recuperationDocuments()
    
    def connexion(self):
        self.reddit = praw.Reddit(client_id='xFYa8Z8tZRG71TFbhGROLQ', client_secret='tR-4GMsMJNZx6wzQFGYYAp5ClUl0Ag', user_agent='WebScrapping_TP_1_2')
    
    def recuperationDocuments(self):
        top_posts = self.reddit.subreddit(self.theme).top('all',limit=self.nbDocuments)
        for post in top_posts:
            self.documents.append(post.title)
        
class ArxivDocuments(Documents):
    # nbDocuments -> nombre de documents Reddit à récupérer
    
    def __init__(self, nbDocuments):
        super().__init__()
        self.nbDocuments = nbDocuments
        self.connexion()
        self.recuperationDocuments()
        
    def connexion(self):
        url = 'http://export.arxiv.org/api/query?search_query=all:' + self.theme + '&start=0&max_results=' + str(self.nbDocuments)
        self.data = urllib.request.urlopen(url)
        
    def recuperationDocuments(self):
        docsTmp = xmltodict.parse(self.data)['feed']['entry']
        # S'il y a 1 document, docTmp prend la forme d'un document, sinon d'une liste
        if(self.nbDocuments == 1):
            self.documents.append(docsTmp['summary'])
        else:
            for docTmp in docsTmp:
                self.documents.append(docTmp['summary'])