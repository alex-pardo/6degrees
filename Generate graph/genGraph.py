
from twython import Twython, TwythonError
import networkx as nx
from time import sleep
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
	iter_count = 0
	request_count = 0
	while len(not_visited) != 0 or iter_count > 1000: 
		current = not_visited.pop(0)
		if current not in visited:

			visited.append(current)
			if request_count >= 14:
				try:
					twitter = connectTwitter()
				except Exception,e:
					print str(e)
				request_count = 0
			loop = 1
			while loop == 1:
				try:
					full_friends = twitter.get_friends_ids(user_id=current, count=5000)
					full_followers = twitter.get_followers_ids(user_id=current, count=5000)
					request_count += 2
					loop = 0
					print 'Read'
				except Exception,e:
					print str(e)
					sleep(960)
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
					not_visited.append(user)
					G.add_edge(current, user)
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
