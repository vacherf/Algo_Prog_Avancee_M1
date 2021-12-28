# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 17:42:27 2021

@author: rpons
"""

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout 

G = nx.Graph()
G.add_edge("avion", "bateau", weight=5)
G.add_edge("avion", "moto",weight=3)
G.add_edge("voiture","avion",weight=2)
try :
    G["voiture"]["avion"]["weight"]+=1
except KeyError: 
    print("test")

print( G["voiture"]["avion"]["weight"])