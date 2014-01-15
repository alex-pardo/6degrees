import networkx as nx
import copy
import random
import operator
import matplotlib.pyplot as plt
import numpy as numpy


###############################
#			MAIN
###############################

def main(NUM_ANTS = 100, ITERATIONS = 10, GAMMA = 0.5, INCREMENT = 1, ANTS_PER_TURN = 100):

	# Read the graph

	G = nx.read_gpickle("mutual.gpickle")
	#G = nx.Graph()
	#G.add_nodes_from(range(1,9))

	#G.add_edges_from([(1,2),(2,3),(3,4),(1,8),(1,5),(8,5),(5,2),(2,7),(7,3),(2,6)])

	# Initialize vars

	results = []
	total_ants = 0

	# REPEAT A CERTAIN NUMBER OF TIMES (to acquire mean results)
	for iter in range(0, ITERATIONS):

		# Initialize the pheromone matrix (weights of the transition fo the edges) to 1

		pheromone = {} # adjacency matrix
		for node in G.nodes():
			for neigh in G.neighbors(node):
				pheromone[str(node)+','+str(neigh)] = 1

		# Setup start and end points
		start = random.choice(G.nodes())
		end = start
		while end == start:
			end = random.choice(G.nodes())
		print 'Finding path between ', str(start), 'and', str(end)

		# Setup the ants (initialize the current_node param. & the objective)
		ants = []
		for a in range(0, ANTS_PER_TURN):
			ants.append(Ant(G, INCREMENT))
			
			ants[a].setStart(start)
			ants[a].setObjective(end)
			total_ants += 1

		# WHILE not (all ants reached the objective)
		while len(ants) > 0:
			a = len(ants)
			while total_ants < NUM_ANTS and len(ants) < ANTS_PER_TURN:
				ants.append(Ant(G, INCREMENT))
				ants[a].setStart(G.nodes()[1])
				ants[a].setObjective(G.nodes()[4])
				a += 1
				total_ants += 1

			# Decrease the pheromone on each position (because of time)
			decreasePheromone(pheromone, GAMMA)
			pheromone_update = {}
			# Run all the ants one step (concurrently?? -> be careful with writing to pheromone matrix -> use a temporal_matrix?)
			deleting_list = []
			for a in range(0, len(ants)):
				pheromone_update = ants[a].step(pheromone, pheromone_update)
				if ants[a].hasReachedObjective():
					deleting_list.append(a)
			if len(deleting_list) > 0:
				for ant in deleting_list[::-1]:
					pheromone_update = ants[ant].returnToStart(pheromone)
					del(ants[ant])
			pheromone = combineDics(pheromone, pheromone_update)

		# END WHILE
		print 'All ants ended'
		# Recover the path with higher weight (greedy)

		result = recoverPath(pheromone, str(start), str(end))
		print 'Best path:', result
		results.append(result)
		print '---------'
	# Get mean results
	edge_labels = {}
	for key in pheromone.keys():
		tmp = key.split(',')
		edge_labels[(int(tmp[0]),int(tmp[1]))] = round((pheromone[key]/float(max(pheromone.values())))*100)/100
		G[int(tmp[0])][int(tmp[1])]['weight'] = round((pheromone[key]/float(max(pheromone.values())))*100)/100
	node_labels = {}
	for i in range(1,9):
		node_labels[i] = str(i)

	#pos = nx.spring_layout(G, scale=20)
	
	# nx.draw_networkx_nodes(G, pos)
	# nx.draw_networkx_edges(G,pos)
	# nx.draw_networkx_labels(G, pos, node_labels, font_size=16)
	# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
	# plt.axis('off')
	# plt.show()

	print 'FINAL MEAN RESULTS:' , numpy.mean(results), '\nWITH STD. DEVIATION:', numpy.std(results)


def decreasePheromone(pheromone, gamma):

	new = copy.deepcopy(pheromone)
	for key in pheromone.keys():
		new[key] = pheromone[key] - gamma# * pheromone[key]
	return new


def recoverPath(pheromone, start, objective):
	current = start
	visited = []
	length = 0
	last = []
	while current != objective:
		visited.append(current)
		candidates = {}
		for key in pheromone.keys():
			if key.startswith(current):
				if key.split(',')[1] not in visited:
					candidates[key] = pheromone[key]
		if len(candidates.keys()) == 0:
			current = last[0]
			length += 1
		else:
			tmp = max(candidates.iteritems(), key=operator.itemgetter(1))[0]
			last.insert(0,current)
			current = tmp.split(',')[1]
			length += 1
	return length

		

def getMean(results):
	tmp = results
	for i in range(len(tmp)-1, 0,-1):
		if tmp[i] == -1:
			del(tmp[i])
	return sum(tmp) / float(len(tmp))

def combineDics(D1, D2):
	for new_value in D2.keys():
		try:
			D1[new_value] = D1[new_value] + D2[new_value]
		except Exception, e: # should never happen
			D1[new_value] = D2[new_value]
	return D1
		

###############################
#			ANT
###############################			


class Ant():
    def __init__(self, G, increment):
        self.start = 0
        self.objective = 0
        self.graph = G
        self.increment = increment
        self.path = []
        
    def setStart(self, start):
    	self.start = start
    	self.current = start
    	self.path.append(self.start)


    def setObjective(self, objective):
    	self.objective = objective

    def step(self, pheromone, new):

    	# From the current node, decide which neighbour to choose using the weights of the edges as the probability of going in this direction	
    	neigh = []
    	probs = []
    	for neighbour in self.graph.neighbors(self.current):
    		neigh.append(neighbour)
    		probs.append(int(pheromone.get(self.current, neighbour)))
    		

    	candidate = self.chooseNeighbour(probs)
    	# Leave a pheromone on the edge
    	try:
    		tmp = new[str(current)+str(neigh[candidate])]
    	except Exception, e:
    		tmp = 0
    	new[str(self.current) + ','+str(neigh[candidate])] = tmp + self.increment

    	# update current node
    	self.current = neigh[candidate]
    	self.path.append(self.current)
    	# return the new weights
    	return new

    def chooseNeighbour(self, probs): # Look at test.py 
    	try:
    		tmp = sum(probs)
    	except Exception, e:
    		print probs
    	
    	for i in range(0, len(probs)):
    		probs[i] /= float(tmp)
    	r = random.random()
    	ranges = [0]
    	for i in range(0, len(probs)):
    		ranges.append(ranges[i]+probs[i])
    		if r <= (ranges[i]+probs[i]) and r > ranges[i]:
    			return i
	
    def hasReachedObjective(self):
    	return self.current == self.objective
	
    def returnToStart(self, pheromone):
    	for pos in xrange(len(self.path)-1, 1, -1):
    		pheromone[str(self.path[pos-1]) +','+str(self.path[pos])] += self.increment
    	return pheromone
    	


main()






