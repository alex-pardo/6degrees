import networkx as nx




###############################
			MAIN
###############################

def main(NUM_ANTS = 100, ITERATIONS = 10, GAMMA = 0.01, INCREMENT = 0.5):

	# Read the graph

	G = nx.read_gpickle("mutual.gpickle")

	# Initialize vars

	results = []

	# REPEAT A CERTAIN NUMBER OF TIMES (to acquire mean results)
	for iter in range(0, ITERATIONS):

		# Initialize the pheromone matrix (weights of the transition fo the edges) to 1

		# TODO

		############################### CHANGE BY A HASHMAP WITH THE NODE ID AS INPUT

		##pheromone = [[1] * len(G.nodes())] * len(G.nodes()) # adjacency matrix

		# Setup the ants (initialize the current_node param. & the objective)

		ants = []
		for a in range(0, NUM_ANTS):
			ants.append(Ant(G))

		# WHILE not (all ants reached the objective)
		while len(ants) > 0:

			# Decrease the pheromone on each position (because of time)
			decreasePheromone(pheromone, GAMMA)
			pheromone_update = self.copyHashMap(pheromone)
			# Run all the ants one step (concurrently?? -> be careful with writing to pheromone matrix -> use a temporal_matrix?)
			for a in range(0, len(ants)):
				pheromone_update = ants[a].step(pheromone, pheromone_update)
				if ants[a].hasReachedObjective():
					del(ants[a])
			pheromone = combineHashMaps(pheromone, pheromone_update)

		# END WHILE

		# Recover the path with higher weight (greedy)

		result = recoverPath(pheromone, start, end)
		results.append(result)
	# Get mean results
	print getMean(results)


def decreasePheromone(pheromone, gamma):

	new = pheromone
	for i in range(0, len(pheromone)):
		tmp = pheromone[i]
		for j in range(0, len(tmp)):
			new[i][j] -= gamma * tmp[j]

	return new


def recoverPath(pheromone, start, objective):
	return 0

def getMean(results):
	return 0

def combineHashMaps(M1, M2):
	return 0

###############################
			ANT
###############################			


class Ant():
    def __init__(self, G, increment):
        self.start = 0
        self.objective = 0
        self.graph = G
        self.increment = increment
        
    def setStart(self, start):
    	self.start = start
    	self.current = start

    def setObjective(self, objective):
    	self.objective = objective

    def step(self, pheromone, new):

    	# From the current node, decide which neighbour to choose using the weights of the edges as the probability of going in this direction	
    	neigh = []
    	probs = []
    	for neighbour in G.getNeighbors(self.current):
    		neigh.appen(neighbour)
    		probs.append(pheromone.get(current, neighbour))

    	candidate = self.chooseNeighbour(probs)
    	# Leave a pheronomone on the edge
    	tmp = new.remove(current, neigh[candidate])
    	new.add(current, neigh[candidate], tmp + self.increment)

    	# update current node
    	self.current = neigh[candidate]

    	# return the new weights
    	return new


    def copyHashMap(self,H):
    	return H

    def chooseNeighbour(self, probs): # Look at test.py 
    	tmp = sum(probs)
		for i in range(0, len(probs)):
			probs[i] /= float(tmp)
		r = random.random()
		ranges = [0]
		for i in range(0, len(probs)):
			ranges.append(ranges[i]+probs[i])
			if r <= (ranges[i]+probs[i]) and r > ranges[i]:
				return i
	

	










