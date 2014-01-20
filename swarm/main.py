'''
Implementation of the Ant Colony Optimization problem to check the six degree theory in a network like Twitter or BlogCatalog.
@autor: Alex Pardo Fernandez: alexpardo.5@gmail.com
@autor: David Sanchez Pinsach: sdividis@gmail.com

'''
import networkx as nx  
import copy
import random
import operator
import matplotlib.pyplot as plt
import numpy as numpy
import os
from threading import Thread
from itertools import chain


system_pheromone = 0 # Global variable of the pheromone in the system
normalization_factor = 1 # Normalization factor at each epoch
epoch = 0 # Current epoch of the system

'''
Main function that provides the degrees between two nodes
@param NUM_ANTS: Maximum number of the ants in the system
@param ITERATIONS: Number of the experiments
@param DECAY: Factor of evaporation of the pheromones
@param INCREMENT: Number of the increment of the pheromones
@param ANTS_PER_TURN: Number of ants at each turn that appears
@param MAX_EPOCH: Number of the iterations at each experiment
'''    

def main(NUM_ANTS = 10000000, ITERATIONS = 50, DECAY = 0.01, INCREMENT = 1, ANTS_PER_TURN = 5, MAX_EPOCH = 100):
	
    # Read the graph from a gpickle file
	G = nx.read_gpickle("mutual.gpickle")
	print 'Reading edges from file'
	G = nx.read_edgelist(os.getcwd()+"/BlogCatalog/edges.csv", delimiter=",", nodetype=int)
	print 'Graph loaded'
	print 'Nodes: ', G.number_of_nodes()
	
	global system_pheromone #Declare a global property of the pheromone in the system
	system_pheromone = G.number_of_edges()
	print 'Edges:', system_pheromone

	# Initialize vars
	results = []
	best_path = float('inf')
	iterations_finished = 0
	# REPEAT A CERTAIN NUMBER OF TIMES (to acquire mean results)
	while iterations_finished < ITERATIONS:

		total_ants = 0
		finished_ants = 0
		total_length = 0
		shortest_path = float('inf')
		# Initialize the pheromone matrix (weights of the transition fo the edges) to 1
		pheromone = {} # adjacency matrix
        
		# Setup start and end points
		start = random.choice(G.nodes())
		while G.neighbors(start) < 7:
			start = random.choice(G.nodes())
		end = start
		while end == start or G.neighbors(end) < 7:
			end = random.choice(G.nodes())

		print 'Finding path between ', str(start), 'and', str(end)
		# Setup the ants (initialize the current_node param. & the objective)
		ants = []
		for a in range(0, ANTS_PER_TURN):
			ants.append(Ant(G, INCREMENT))
			ants[a].setStart(start)
			ants[a].setObjective(end)
			total_ants += 1
		global epoch
		epoch = 0
		ants_finish_last_turn = 0
		ants_end = 0
		# WHILE not (all ants reached the objective)
		while (epoch < MAX_EPOCH and len(ants) > 0) or ants_end == 0:
			epoch += 1
			a = len(ants)
			tmp_counter = 0
			while total_ants < NUM_ANTS and tmp_counter < ANTS_PER_TURN:
				ants.append(Ant(G, INCREMENT))
				ants[a].setStart(start)
				ants[a].setObjective(end)
				a += 1
				total_ants += 1
				tmp_counter += 1

			# Decrease the pheromone on each position (because of time) and maintain the system pheromone
			pheromone = normalizePheromone(pheromone, DECAY, len(ants)+ants_finish_last_turn, INCREMENT)
			pheromone_update = copy.deepcopy(pheromone)
			# Run all the ants one step (concurrently?? -> be careful with writing to pheromone matrix -> use a temporal_matrix?)
			for a in range(0, len(ants)):
				tmp = ants[a].step(pheromone, DECAY)#, returned_matrices, a)
				pheromone_update = dict(chain(pheromone_update.items(), tmp.items()))
			
			pheromone = dict(chain(pheromone.items(), pheromone_update.items()))
			ants_finish_last_turn = 0
   			for a in xrange(len(ants)-1,0,-1):
				if ants[a].hasReachedObjective():
					
					tmp = ants[a].returnToStart(pheromone)
					tmp_len = tmp['len']
					if tmp_len > 0:
						pheromone.update(tmp['pheromone'])
						ants_finish_last_turn += tmp_len
						total_length += tmp_len
						finished_ants += 1
						if tmp_len < shortest_path:
							shortest_path = tmp_len
					del(ants[a])
					total_ants -= 1
					ants_end += 1
		# END WHILE
		print 'All ants ended'

		# Recover the path with higher weight (greedy)
		try:
			result = total_length/float(finished_ants)
			print 'Avg. path:', result
			print 'Shortest path:', shortest_path
			if shortest_path < best_path:
				best_path = shortest_path
			results.append(shortest_path)
			iterations_finished += 1
		except Exception, e:
			pass
			#print 'None of the ants have finished :('
		print '---------'
	print 'FINAL MEAN SHORTEST PATH:' , numpy.mean(results), '\nWITH STD. DEVIATION:', numpy.std(results)
	print 'FINAL SHORTEST PATH', best_path


''' Method to normalize all pheromone in the system'''
def normalizePheromone(pheromone, decay, num_ants, update):
	#new = copy.deepcopy(pheromone)
	new_pheromone = float(num_ants*update*(1-decay))
	nu = (new_pheromone + system_pheromone) / float(system_pheromone)
	global normalization_factor
	normalization_factor = nu
	pheromone.update((x, (y*(1-decay))/float(nu)) for x, y in pheromone.items())
	return pheromone

''' Method to recover the path between two nodes'''
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


''' Method to get the mean value of the results''' 
def getMean(results):
	tmp = results
	for i in range(len(tmp)-1, 0,-1):
		if tmp[i] == -1:
			del(tmp[i])
	return sum(tmp) / float(len(tmp))

''' Method to join dictionaries in one'''
def combineDics(D1, D2):
	D = dict(chain(D1.items(), D2.items()))
	return D
		

###############################	
''' Ant class'''		
class Ant():
    
    ''' Construct of the ant class'''
    def __init__(self, G, increment):
        self.start = 0
        self.objective = 0
        self.graph = G
        self.increment = increment
        self.path = []
        
    '''Method to set the start node point'''
    def setStart(self, start):
    	self.start = start
    	self.current = start
    	self.path.append(self.start)

    '''Method to set the objective node point'''
    def setObjective(self, objective):
    	self.objective = objective

        
    '''From the current node, decide which neighbour to choose using the
    weights of the edges as the probability of going in this direction	'''
    def step(self, pheromone, decay):#, result, index):
    	neigh = []
    	probs = []
    	new = {}
    	for neighbour in self.graph.neighbors(self.current):
    		neigh.append(neighbour)
    		try:
    			probs.append(float(pheromone[str(self.current)+','+ str(neighbour)]))
    		except Exception, e:
    			probs.append(1)
    		
    	candidate = self.chooseNeighbour(probs)
    	# Leave a pheromone on the edge
    	try:
    		tmp = new[str(current)+','+str(neigh[candidate])]
    	except Exception, e:
    		tmp = ((1-decay)**epoch) / float(normalization_factor)
    	new[str(self.current) + ','+str(neigh[candidate])] = tmp + self.increment

    	# update current node
    	self.current = neigh[candidate]
    	self.path.append(self.current)
    	# return the new weights
    	return new

    '''Method to choose the neighbour step with certain probabilities'''
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
	
    '''Method to check if the ant arrives to the objective or not'''
    def hasReachedObjective(self):
    	if len(self.path) > 15:
    		return True
    	return self.current == self.objective
	
    '''Method to return the ant to the initial point'''
    def returnToStart(self, pheromone):
    	if len(self.path) > 15:
    		return {'len':-1, 'pheromone':pheromone}
    	for pos in xrange(len(self.path)-1, 1, -1):
    		try:
    			pheromone[str(self.path[pos-1]) +','+str(self.path[pos])] += self.increment
    		except Exception, e: # Should never happen!
    			pheromone[str(self.path[pos-1]) +','+str(self.path[pos])] = 1 + self.increment		
    	return {'len':len(self.path), 'pheromone':pheromone}
    	
main()