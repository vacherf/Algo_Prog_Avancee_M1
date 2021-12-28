from Auteur import Auteur
from Document import RedditDocument
from Document import ArxivDocument
from Corpus import Corpus
import urllib.request
import xmltodict
from dateutil.parser import parse
import pickle
from datetime import datetime
import praw
import re
# import pandas

# Dictionnaire ayant comme clé un id et comme valeur le titre du document
id2doc = {}
idDoc = 0

# Liste contenant tous les documents récupérés
collection = []

# Dictionnaire ayant comme clé un id et comme valeur un auteur
authors = {}

# Dictionnaire ayant comme clé un id et comme valeur le nom de l'auteur
id2aut = {}

def auteurExiste(auteur):
    for key, author in id2aut.items():
        if author == auteur:
            return key
    return -1

def ajouterDoc(document):
    global idDoc
    id2doc[idDoc] = document.titre
    idDoc += 1
    collection.append(document)

def ajouterRedditDocument(document):
    ajouterDoc(document)
    indexAuteur = auteurExiste(document.auteur)
    if indexAuteur == -1:
        authors[len(authors)] = Auteur(document.auteur, 1, [document])
        id2aut[len(authors) - 1] = str(document.auteur)
    else:
        authors[indexAuteur].ndoc += 1
        authors[indexAuteur].add(document)

def ajouterArxivDocument(document, auteurs):
    ajouterDoc(document)
# =============================================================================
#     for auteur in auteurs:
#         if(auteur):
#             indexAuteur = auteurExiste(auteur['name'])
#             print(indexAuteur)
#             if indexAuteur == -1:
#                 authors[len(authors)] = Auteur(auteur['name'], 1, [document])
#                 if nature == 'Arxiv':
#                     document.addCoAuteur(auteur)
#                 id2aut[len(authors) - 1] = auteur['name']
#             else:
#                 authors[indexAuteur].ndoc += 1
#                 authors[indexAuteur].add(document)
# =============================================================================

def conversionDate(date):
    dt = parse(date)
    return dt.strftime('%d/%m/%Y')

theme = "robotics"

# Reddit connexion
reddit = praw.Reddit(client_id='xFYa8Z8tZRG71TFbhGROLQ', client_secret='tR-4GMsMJNZx6wzQFGYYAp5ClUl0Ag', user_agent='WebScrapping_TP_1_2')

nbResultReddit = 1

docs = []
top_posts = reddit.subreddit(theme).top('all',limit=nbResultReddit)
for post in top_posts:
    docs.append(('Reddit', post))

nbResultArxiv = 6

url = 'http://export.arxiv.org/api/query?search_query=all:' + theme + '&start=0&max_results=' + str(nbResultArxiv)
data = urllib.request.urlopen(url)

docs2 = xmltodict.parse(data)['feed']['entry']
if(nbResultArxiv == 1):
    docs.append(('Arxiv', docs2))
else:
    for doc2 in docs2:
        docs.append(('Arxiv', doc2))

for nature, doc in docs:
    docTmp = ''
    if nature == 'Reddit':
        dateTmp = datetime.utcfromtimestamp(doc.created_utc).strftime('%d/%m/%Y')
        docTmp = RedditDocument(doc.title, dateTmp, doc.url, doc.selftext, doc.author, doc.num_comments)
        ajouterRedditDocument(docTmp)
    elif nature == 'Arxiv':
        docTmp = ArxivDocument(doc['title'], conversionDate(doc['published']), doc['id'], doc['summary'])
        ajouterArxivDocument(docTmp, doc['author'])

# =============================================================================
# print("Id2Doc : " + str(id2doc) + "\n")
# =============================================================================

def getTexteGlobal():
    texteGlobal = ""
    for doc in collection:
        if doc.texte != "":
            texteGlobal += doc.texte + " "
    return texteGlobal

# print("Collection : ")
# for doc in collection:
#     print(type(doc))
#     print(str(doc) + "\n")

# =============================================================================
# print("Authors : ")
# for i in range(len(authors)):
#     print(str(authors[i]) + "\n")
# 
# print("Id2aut : " + str(id2aut) + "\n")
# =============================================================================

corp = Corpus('Corpus 1', authors, id2aut, id2doc)
# for document in corp.afficherDocuments(100):
#     if document.getType() == "Arxiv":
#         print(ArxivDocument.__repr__(document))
#     else:
#         print(RedditDocument.__repr__(document))
#
# # Sauvegarde
# with open("corpus.pkl", "wb") as f:
#     pickle.dump(corp, f)

# del corp
#
# with open("corpus.pkl", "rb") as f:
#     res = pickle.load(f)
#
# print("Element présent dans la sauvegarde : \n")
# for document in res.afficherDocuments(10):
#     print(repr(document))

# Récupération de tous les textes dans une seule chaine de caractère
# =============================================================================
# texteGlobal = getTexteGlobal()
# t = re.finditer("effect", texteGlobal)
# print(t)
# for t_bis in t:
#     print(t_bis.end())
# =============================================================================
# print(f)

# corp.concorde("to", texteGlobal, 20)

# =============================================================================
# print(collection)
# =============================================================================
corp.creationGraphe(collection)