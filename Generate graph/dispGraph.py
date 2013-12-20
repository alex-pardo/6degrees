import networkx as nx
import matplotlib.pyplot as plt
import pylab as P
#def main():

G=nx.read_gpickle("mutual.gpickle")

print(nx.average_shortest_path_length(G))

nx.draw(G)

plt.show()



