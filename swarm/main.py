import networkx as nx
import copy
import random
import operator
import matplotlib.pyplot as plt
import numpy as numpy
import os
from threading import Thread
from itertools import chain

###############################
#			MAIN
###############################
system_pheromone = 0
normalization_factor = 1
epoch = 0
def main(NUM_ANTS = 10000000, ITERATIONS = 10, DECAY = 0.01, INCREMENT = 1, ANTS_PER_TURN = 10, MAX_EPOCH = 500):

	# Read the graph

	G = nx.read_gpickle("mutual.gpickle")
	print 'Reading edges from file'
	G = nx.read_edgelist(os.getcwd()+"/BlogCatalog/edges.csv", delimiter=",", nodetype=int)
	print 'Graph loaded'
	print 'Nodes: ', G.number_of_nodes()
	
	global system_pheromone
	system_pheromone = G.number_of_edges()
	print 'Edges:', system_pheromone
	
	

	# Initialize vars

	results = []
	best_path = float('inf')
	iterations_finished = 0
	# REPEAT A CERTAIN NUMBER OF TIMES (to acquire mean results)
	#for iter in range(0, ITERATIONS):
	while iterations_finished < ITERATIONS:

		total_ants = 0
		finished_ants = 0
		total_length = 0
		shortest_path = float('inf')
		# Initialize the pheromone matrix (weights of the transition fo the edges) to 1

		pheromone = {} # adjacency matrix
		# for node in G.nodes():
		# 	for neigh in G.neighbors(node):
		# 		pheromone[str(node)+','+str(neigh)] = 1

		# Setup start and end points
		start = random.choice(G.nodes())
		while G.neighbors(start) < 4:
			start = random.choice(G.nodes())
		end = start
		while end == start or G.neighbors(end) < 4:
			end = random.choice(G.nodes())

		print 'Finding path between ', str(start), 'and', str(end)

		#threads = [None] * NUM_ANTS
		#returned_matrices = [None] * NUM_ANTS
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
		# WHILE not (all ants reached the objective)
		while epoch < MAX_EPOCH and len(ants) > 0:
			#if epoch%10 == 0:
			# print len(ants)
			# print epoch
			# print len(pheromone)
			# print '----'
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
			
				#threads[a] = Thread(target=ants[a].step, args=(pheromone, returned_matrices, a))
				#threads[a].start()

			#for a in range(len(ants)):
			#	threads[a].join()
			
			#for i in range(len(ants)):
			#	pheromone = combineDics(pheromone, returned_matrices[i])
			pheromone = dict(chain(pheromone.items(), pheromone_update.items()))
			ants_finish_last_turn = 0
   			for a in xrange(len(ants)-1,0,-1):
				if ants[a].hasReachedObjective():
					
					tmp = ants[a].returnToStart(pheromone)
					tmp_len = tmp['len']
					if tmp_len > 0:
						pheromone.update(tmp['pheromone'])
						print 'ANT ENDS'
						print tmp_len
						ants_finish_last_turn += tmp_len
						total_length += tmp_len
						finished_ants += 1
						if tmp_len < shortest_path:
							shortest_path = tmp_len
						#pheromone = combineDics(pheromone, pheromone_update)
					del(ants[a])
					#del(threads[a])
					#del(returned_matrices[a])
					total_ants -= 1


			# for a in range(0, len(ants)):
			# 	pheromone_update = ants[a].step(pheromone, pheromone_update)
			# 	if ants[a].hasReachedObjective():
			# 		deleting_list.append(a)
			# if len(deleting_list) > 0:
			# 	for ant in deleting_list[::-1]:
			# 		pheromone_update = ants[ant].returnToStart(pheromone)
			# 		del(ants[ant])
			# pheromone = combineDics(pheromone, pheromone_update)

		# END WHILE
		print 'All ants ended'

		# Recover the path with higher weight (greedy)
		#result = recoverPath(pheromone, str(start), str(end))
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
	# Get mean results
	# edge_labels = {}
	# for key in pheromone.keys():
	# 	tmp = key.split(',')
	# 	edge_labels[(int(tmp[0]),int(tmp[1]))] = round((pheromone[key]/float(max(pheromone.values())))*100)/100
	# 	G[int(tmp[0])][int(tmp[1])]['weight'] = round((pheromone[key]/float(max(pheromone.values())))*100)/100
	# node_labels = {}
	# for i in range(1,9):
	# 	node_labels[i] = str(i)

	# pos = nx.spring_layout(G, scale=20)
	
	# nx.draw_networkx_nodes(G, pos)
	# nx.draw_networkx_edges(G,pos)
	# nx.draw_networkx_labels(G, pos, node_labels, font_size=16)
	# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
	# plt.axis('off')
	# plt.show()

	print 'FINAL MEAN SHORTEST PATH:' , numpy.mean(results), '\nWITH STD. DEVIATION:', numpy.std(results)
	print 'FINAL SHORTEST PATH', best_path


def normalizePheromone(pheromone, decay, num_ants, update):

	#new = copy.deepcopy(pheromone)
	new_pheromone = float(num_ants*update*(1-decay))
	nu = (new_pheromone + system_pheromone) / float(system_pheromone)
	global normalization_factor
	normalization_factor = nu
	pheromone.update((x, (y*(1-decay))/float(nu)) for x, y in pheromone.items())
	return pheromone
	# for key in pheromone.keys():
	# 	new[key] = (pheromone[key] * (1-decay))/float(nu)
	# return new


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
					#try:
					#	pheromone.pop(key,None)
					#except:
					#	print 'except'
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

	D = dict(chain(D1.items(), D2.items()))

	return D

	# for new_value in D2.keys():
	# 	try:
	# 		D1[new_value] = float(D1[new_value] + D2[new_value])
	# 	except Exception, e: 
	# 		D1[new_value] = float(D2[new_value])
	# return D1
		

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

    def step(self, pheromone, decay):#, result, index):

    	# From the current node, decide which neighbour to choose using the weights of the edges as the probability of going in this direction	
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
    	#result[index] = new

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
    	if len(self.path) > 15:
    		return True
    	return self.current == self.objective
	
    def returnToStart(self, pheromone):
    	if len(self.path) > 15:
    		return {'len':-1, 'pheromone':pheromone}
    	for pos in xrange(len(self.path)-1, 1, -1):
    		try:
    			pheromone[str(self.path[pos-1]) +','+str(self.path[pos])] += self.increment
    		except Exception, e: # should never happen!
    			pheromone[str(self.path[pos-1]) +','+str(self.path[pos])] = 1 + self.increment
	    		
    	return {'len':len(self.path), 'pheromone':pheromone}
    	


main()






