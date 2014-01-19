import networkx as nx  
import matplotlib.pyplot as plt
import numpy as numpy
import os


G = nx.read_edgelist(os.getcwd()+"/BlogCatalog/edges.csv", delimiter=",", nodetype=int)
#pos = nx.spring_layout(G)
print 'draw'
nx.draw(G)
print 'saving'
#nx.draw_networkx_edges(G,pos)
plt.savefig("graph.png",bbox_inches="tight")
pylab.close()