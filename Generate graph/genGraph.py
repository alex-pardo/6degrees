
from twython import Twython, TwythonError
import networkx as nx
from time import sleep
import random
#import pylab as P
import matplotlib.pyplot as plt

def main():
	MAX_ITER = 150
	try:
		G = nx.read_gpickle("mutual.gpickle")
		not_visited = [G.nodes()[len(G.nodes())-1]]
	except:
		G = nx.Graph()
		not_visited = ['165916420']
	visited = []

	twitter = connectTwitter()
	first = 1
	iter_count = 0
	request_count = 0
	while len(not_visited) != 0 and iter_count < MAX_ITER: 
		current = not_visited.pop(0)
		if current not in visited:

			visited.append(current)
			
			loop = 1
			while loop == 1:
				try:
					full_friends = twitter.get_friends_ids(user_id=current, count=100)
					full_followers = twitter.get_followers_ids(user_id=current, count=100)
					loop = 0
					print 'Read'
				except Exception,e:
					print str(e)
					if first == 1:
						print 'drawing...'
						nx.draw(G)  # networkx draw()
						plt.show() 
						first = 0
					sleep(60)
					try:
						twitter = connectTwitter()
					except Exception,e:
						print str(e)

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
					#print 'Add edge between', current , ' and ', user 
			iter_count += 1
			nx.write_gpickle(G,"mutual.gpickle")

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


main()
