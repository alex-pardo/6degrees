
from twython import Twython, TwythonError
import networkx as nx
from time import sleep
import random
from random import choice
#import pylab as P
import matplotlib#.pyplot as plt
import pylab as P
import pickle

def main():
	MAX_ITER = 150
	try:
		G = nx.read_gpickle("mutual.gpickle")
		not_visited = readList()
	except:
		print 'No stored information'
		G = nx.Graph()
		not_visited = ['165916420']
	visited = []
	if len(not_visited) == 0:
		not_visited = ['165916420']
	twitter = connectTwitter()
	first = 1
	iter_count = 0
	request_count = 0
	while len(not_visited) != 0 and iter_count < MAX_ITER: 
		current = choice(not_visited)
		if current not in visited:

			visited.append(current)
			loop = 1
			while loop == 1:
				try:
					full_friends = twitter.get_friends_ids(user_id=current, count=100)
					full_followers = twitter.get_followers_ids(user_id=current, count=100)
					loop = 0
					first = 1
				except Exception,e:
					print 'E1:', str(e)
					if first == 1:
						#print 'drawing...'

						try:
							#plotGraph(G)
							print 'Saving data'
							saveData(G, not_visited)
						except Exception, e3:
							print 'No graph for drawing :( '
						first = 0
					if '401' in str(e): #401 error needs to reauthenticate
						try:
							print 'Reconnecting...'
							twitter = connectTwitter()

						except Exception,e2:
							print 'E2:', str(e2)
					else:
						sleep(960)
					#successful = 0
					#while successful == 0:
					#	try:
					#		twitter = connectTwitter()
					#		successful = 1
					#	except Exception,e2:
					#		print 'E2:', str(e2)
					#		sleep(30)
			print 'Information read'
			friends = []
			followers = []
			for user in full_friends['ids']:
				friends.append(user)
			for user in full_followers['ids']:
				followers.append(user)

			for user in friends:
				if user in followers: # Mutual friends are those the user is following and they are following the user back
					G.add_edge(current, user)
					if random.random() <= 0.3:
						not_visited.append(user)
						for node in G.nodes():
							if G.neighbors(node) <= 2:
								if node not in not_visited:
									not_visited.append(node)
			iter_count += 1
	p.join
			
	
def plotGraph(G):
	print(nx.average_shortest_path_length(G))
	pos=nx.graphviz_layout(G,prog="twopi",root=G.nodes()[0])
	nx.draw(G,pos,with_labels=False,alpha=0.5,node_size=15)
	P.show()

def connectTwitter():
	APP_KEY = 'ORbbZFlJWipi3HFblfPuQ'
	APP_SECRET = 's2em5f68RBV8UDgW7iXOH5PMFArF5aVj8GG6IgsU'

	twitter = Twython(APP_KEY, APP_SECRET)

	print 'Connecting...'
	auth = twitter.get_authentication_tokens()

	OAUTH_TOKEN = '165916420-31NTOhsitabrC6tgo0Zd87q0f60mGUdjBZan56HQ'
	OAUTH_TOKEN_SECRET = '8gpWg3g207b4QMuabv2xkw2VkkMyBPnDEImTquPgZC0vV'

	# Requires Authentication as of Twitter API v1.1
	twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	print 'Connected'
	return twitter

def saveData(G, not_visited):
	nx.write_gpickle(G,"mutual.gpickle")
	with open('not_visited', 'wb') as f:
	    	pickle.dump(not_visited, f)

def readList():
	with open('not_visited', 'rb') as f:
	    	not_visited = pickle.load(f)
    	return not_visited

main()
