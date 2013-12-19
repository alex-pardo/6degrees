import networkx as nx
import matplotlib.pyplot as plt

#def main():

G=nx.read_gpickle("mutual.gpickle")

#G=nx.path_graph(8)
nx.draw(G)
plt.show()



