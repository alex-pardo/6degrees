from twython import Twython, TwythonError
import networkx as nx
#import xmlrpclib
import ubigraph
import random
def main():
	APP_KEY = 'ORbbZFlJWipi3HFblfPuQ'
	APP_SECRET = 's2em5f68RBV8UDgW7iXOH5PMFArF5aVj8GG6IgsU'

	twitter = Twython(APP_KEY, APP_SECRET)

	auth = twitter.get_authentication_tokens()

	OAUTH_TOKEN = '165916420-31NTOhsitabrC6tgo0Zd87q0f60mGUdjBZan56HQ'
	OAUTH_TOKEN_SECRET = '8gpWg3g207b4QMuabv2xkw2VkkMyBPnDEImTquPgZC0vV'

	main_user = 100

	# Requires Authentication as of Twitter API v1.1
	twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	try:
	    user_timeline = twitter.get_friends_ids(screen_name='alex_pardo5', count=5000)
		
	except TwythonError as e:
	    print e

	i = 0
	print user_timeline
	#G=nx.Graph()
	
	#G.add_node(main_user)
	#print user_timeline


	#server = xmlrpclib.Server('http://localhost:20738/RPC2')
	#G = server.ubigraph
	G = ubigraph.Ubigraph()

	G.clear()

	main_user = G.newVertex(shape="sphere", color="#ffff00", label='alex_pardo5')
	
	red = G.newVertexStyle(shape="sphere", color="#ff0000", size="1")
	
	for user in user_timeline['ids']:
		#print twitter.show_user(user_id=user)
		#tmp = twitter.show_user(user_id=user)['screen_name']
		tmp = user
		tmp = G.newVertex(style=red, label=str(tmp))
		G.newEdge(main_user,tmp,arrow=True, width=random.randint(1, 5))
		i += 1
	
	print i
	
	#displayGraph(G)
	
def displayGraph(graph):
    import xmlrpclib
    server = xmlrpclib.Server('http://localhost:20738/RPC2')
    G = server.ubigraph
    G.clear()
    vertex = {}

    for edge in graph.edges():
        if not vertex.has_key(edge[0]):
            vertex[edge[0]] = G.new_vertex()
            G.set_vertex_attribute(vertex[edge[0]], 'label', users[edge[0]])
##            if graph.node[edge[0]]['type'] == 'follower':                
##                G.set_vertex_attribute(vertex[edge[0]], 'shape', 'cone')
##                G.set_vertex_attribute(vertex[edge[0]], 'color', '#ff0000')
##            else:
            G.set_vertex_attribute(vertex[edge[0]], 'shape', 'sphere')
            G.set_vertex_attribute(vertex[edge[0]], 'color', '#0000ff')
        if not vertex.has_key(edge[1]):
            vertex[edge[1]] = G.new_vertex()
            G.set_vertex_attribute(vertex[edge[1]], 'label', users[edge[1]])
##            if graph.node[edge[0]]['type'] == 'follower':                
##                G.set_vertex_attribute(vertex[edge[1]], 'shape', 'cone')
##                G.set_vertex_attribute(vertex[edge[1]], 'color', '#ff0000')
##            else:
            G.set_vertex_attribute(vertex[edge[1]], 'shape', 'sphere')
            G.set_vertex_attribute(vertex[edge[1]], 'color', '#0000ff')
        G.new_edge(vertex[edge[0]],vertex[edge[1]])

main()
