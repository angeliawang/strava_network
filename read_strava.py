# note: need to run this as "python3 read_strava.py" and not "python read_strava.py"

import numpy as np
import csv
import networkx as nx
from networkx import *
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite

print("imported networkx")

# This script uses the results output by strava.py and builds the connectivity matrices needed
# We make a bipartite graph: one set is runs, another set is segments
# Connect a node to a segment if that segment is covered during that run

# preserves order
def unique(sequence):
    seen = set()
    return [x for x in sequence if not (x=='' or x in seen or seen.add(x))]

num_runs = 251
num_segments = 221 # found by enumerating through the csv

run_list = np.arange(num_runs)
connectivity = np.zeros((num_runs, num_segments))

my_graph = nx.Graph()
color_list = []

# read in the dates file and make a list of dates
dates = []
with open('all_dates.csv', 'r') as csvfile:
	all_dates = csv.reader(csvfile)
	for date in all_dates:
		rearranged_date = ''.join(date[5:7]+date[8:10]+date[0:4])
		dates.append(rearranged_date) # this is now an 8-character string
# might have duplicates and that's ok 
#print(dates)

all_segments = []
# Fortunately, each row read from the csv file is returned as a list of strings by default
with open('all_segs.csv', 'r') as csvfile:
	all_runs = csv.reader(csvfile)
	for run in all_runs:
		all_segments+=run
segment_list = unique(all_segments)

with open('date_nodes.csv','w') as result_file:
	wr = csv.writer(result_file, dialect='excel')
	for date in dates:
		wr.writerow([date]) 
		# for some reason, if you don't have brackets, it puts everything into its own column

with open('seg_nodes.csv','w') as result_file:
    wr = csv.writer(result_file, dialect='excel')
    for seg in segment_list:
    	wr.writerow([seg])

edge_list = []
# not super efficient, but need to iterate once to build segment_list and another time to populate the connectivity matrix
with open('all_segs.csv', 'r') as csvfile:
	all_runs = csv.reader(csvfile)
	run_index = 0
	for run in all_runs: 
		# print(run)
		for s_i in range(len(run)):
			seg = run[s_i]
			if seg: # because '' apparently is a valid segment
				segment_index = segment_list.index(seg)
				connectivity[run_index, segment_index] = 1

				# add an edge in the graph from the date of that run to the segment
				my_graph.add_node(dates[run_index], day=dates[run_index], cat='date', ncolor=run_index/num_runs)
				color_list.append('b')
				my_graph.add_node(seg, cat='segment')
				color_list.append('r')
				my_graph.add_edge(dates[run_index], seg)
				edge_list.append([dates[run_index], seg])
		run_index += 1
run_distribution = np.sum(connectivity, 1)
seg_distribution = np.sum(connectivity, 0)

with open('all_edges.csv','w') as result_file:
    wr = csv.writer(result_file, dialect='excel')
    for edge in edge_list:
    	edge.append(seg_distribution[segment_list.index(edge[1])])
    	edge.append(run_distribution[dates.index(edge[0])])
    	edge+=['seg', 'run']
    	wr.writerow(edge)

degree_total = np.sum(np.sum(connectivity, 1))

# debugging junk
'''for node in my_graph.nodes(data=True):
	if node[1]['cat']=='date':
		print(node)'''

# to analyze degree distribution
run_distribution = np.sum(connectivity, 1)
seg_distribution = np.sum(connectivity, 0)

#print(seg_distribution)
#print(run_distribution)


# plotting distributions
plt.plot()
plt.hist(np.sort(seg_distribution), bins=range(int(np.amax(seg_distribution))), density=True)
plt.title('Segment degree distribution')
plt.xlabel('degree')
plt.ylabel('relative frequency')
#plt.semilogy()
#plt.semilogx()
plt.show()

plt.plot()
plt.hist(np.sort(run_distribution), bins=range(int(np.amax(run_distribution))), density=True)
plt.title('Run degree distribution')
plt.xlabel('degree')
plt.ylabel('relative frequency')
#plt.semilogy()
#plt.semilogx()
plt.show()

# projection onto a given set of nodes, with weights equivalent to the Jaccard index
# Jaccard index is the ratio of the size of the intersection of the two neighborhoods
# to the union of the two neighborhoods
all_node_data = my_graph.nodes(data=True)

seg_nodes = []
for node in all_node_data:
	node_dict = node[1]
	if node_dict['cat']=='segment':
		seg_nodes.append(node[0])

#print(seg_nodes)
my_graph_projection = bipartite.overlap_weighted_projected_graph(my_graph, seg_nodes)
projected_edges = my_graph_projection.edges(data=True)

proj_list = []
with open('all_proj_edges.csv','w') as result_file:
	wr = csv.writer(result_file, dialect='excel')
	for p_edge in projected_edges:
		add_dis = [p_edge[0], p_edge[1], p_edge[2]['weight']]
		wr.writerow(add_dis)

print("The clustering coefficient of the projection is", nx.average_clustering(my_graph_projection))

print("The shortest average path length for each component in the projection is")
for g in nx.connected_component_subgraphs(my_graph_projection):
	print(nx.average_shortest_path_length(g))

plt.plot()
pos = spring_layout(my_graph_projection)
nodes = draw_networkx_nodes(my_graph_projection, pos, edgecolors='k')
draw_networkx_edges(my_graph_projection, pos)
nx.draw(my_graph, with_labels=False, font_weight='bold')
plt.show()

# some print statements for sanity
'''sum_segments = np.sum(connectivity, 0)
print(run_index)
print(sum_segments)
print(segment_list)'''

# print("The total number of segments is %d\n", len(all_segments)) # 10291
# print("The total number of unique segments is %d\n", len(set(all_segments))) #222

# messing around with functions
'''print(nx.bipartite.color(my_graph)) #True' 
print(nx.bipartite.is_bipartite(my_graph))'''

# attempts at coloring
colorz = np.array([num/(num_runs+num_segments) for num in range(num_segments+num_runs)])
#print(np.shape(colorz))

color_dict = {'0':'b','1':'r'}
#print(my_graph.nodes(data=True)) # which includes the category data

'''color_list =[] #]np.empty([num_segments+num_runs])
i=0
for node in my_graph.nodes(data=True):
	if node[1]['cat']=='segment':
		color_list.append('r')
	elif node[1]['cat']=='date':
		color_list.append('b') #node[1]['ncolor'])
	i+=1'''

# let's look at some numberssss
#X, Y = bipartite.sets(my_graph)
print("The overall clustering coefficient is", bipartite.average_clustering(my_graph))
print("The clustering coefficient of the segment nodes is", bipartite.average_clustering(my_graph, segment_list))
print("The clustering coefficient of the dates is", bipartite.average_clustering(my_graph, dates[0:num_runs]))
print("The clustering coefficient for each connected component is")
for g in nx.connected_component_subgraphs(my_graph):
	print(bipartite.average_clustering(g))

	'''nodes = g.nodes(data=True)
	print(type(nodes))
	these_nodes = [node for node in nodes if node[1]['cat']=='date']
	print("Date avg clust coeff is ", bipartite.average_clustering(g, these_nodes)) 
	those_nodes = [node for node in nodes if node[1]['cat']=='segment']
	print(bipartite.average_clustering(g, those_nodes)) '''

# size of the largest component
print("The size of the largest connected components is", len(nx.node_connected_component(my_graph, 'Sheridan Road Climb')))
print("The size of the smallest connected components is", len(nx.node_connected_component(my_graph, 'Asbury Avenue Climb')))

# number of connected components
print("The total number of ")
print("The number of connected components is", nx.number_connected_components(my_graph))
# for each one, what is the shortest path length?
print("The shortest average path length for each component is")
for g in nx.connected_component_subgraphs(my_graph):
	print(nx.average_shortest_path_length(g)) 

#print(nx.node_connected_component(my_graph, 'Sheridan Road Climb'))

# visualizations
'''pos1 = networkx.drawing.layout.bipartite_layout(my_graph, segment_list)
plt.plot()
nx.draw(my_graph, pos=pos1, with_labels=False, node_color=color_list)
plt.show()

# need to jump through some hoops to put outlines around the nodes
plt.plot()
pos = spring_layout(my_graph)
nodes = draw_networkx_nodes(my_graph, pos, edgecolors='k')
draw_networkx_edges(my_graph, pos)
nx.draw(my_graph, with_labels=False, font_weight='bold', node_color=color_list)
plt.show()'''

print("All set")
