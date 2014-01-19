
import networkx as nx
G = nx.read_gpickle("mutual2.gpickle")
nx.write_edgelist(G, "mutual2.csv", delimiter=',')