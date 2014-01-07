import networkx as nx
import matplotlib.pyplot as plt



def show2D():

	#G = nx.read_gpickle("mutual.gpickle")

	G = nx.Graph()
	G.add_nodes_from(range(1,8))
	G.add_edges_from([(1,2),(2,3),(3,4),(1,8),(1,5),(8,5),(5,2),(2,7),(7,3),(2,6)])

	print(nx.average_shortest_path_length(G))



	pos = nx.spring_layout(G)
	nx.draw_networkx_nodes(G, pos)
	nx.draw_networkx_edges(G,pos)
	labels = {}
	labels[1] = '1'
	labels[2] = '2'
	labels[3] = '3'
	labels[4] = '4'
	labels[5] = '5'
	labels[6] = '6'
	labels[7] = '7'
	labels[8] = '8'
	nx.draw_networkx_labels(G, pos, labels, font_size=16)
	plt.axis('off')
	
	plt.show()





show2D()
 