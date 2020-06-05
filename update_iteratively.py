# updates the network run by run
# need to run it as "python3 update_iteratively.py"

import csv
import networkx as nx
from networkx import *
import matplotlib.pyplot as plt

dates = []
my_graph = nx.Graph()
color_list = []

num_runs = 251
num_segments = 221 # found by enumerating through the csv

# preserves order
def unique(sequence):
	seen = set()
	return [x for x in sequence if not (x=='' or x in seen or seen.add(x))]

with open('all_dates.csv', 'r') as csvfile:
	all_dates = reversed(list(csv.reader(csvfile)))
	for date in all_dates:
		rearranged_date = ''.join(date[5:7]+date[8:10]+date[0:4])
		dates.append(rearranged_date) # this is now an 8-character string

dates = dates[1::]

all_segments = []
# Fortunately, each row read from the csv file is returned as a list of strings by default
with open('all_segs.csv', 'r') as csvfile:
	all_runs = reversed(list(csv.reader(csvfile)))
	for run in all_runs:
		all_segments+=run
segment_list = unique(all_segments)

plt.plot(100)
#plt.ion()
with open('all_segs.csv', 'r') as csvfile:
	all_runs = reversed(list(csv.reader(csvfile)))
	run_index = 0
	for run in all_runs: 
		# print(run)
		for s_i in range(len(run)):
			seg = run[s_i]
			if seg: # because '' apparently is a valid segment
				segment_index = segment_list.index(seg)

				# add an edge in the graph from the date of that run to the segment
				my_graph.add_node(dates[run_index], day=dates[run_index], cat='date', ncolor=run_index/num_runs)
				color_list.append('b')
				my_graph.add_node(seg, cat='segment')
				color_list.append('r')
				my_graph.add_edge(dates[run_index], seg)

				pos = spring_layout(my_graph)
				nodes = draw_networkx_nodes(my_graph, pos, edgecolors='k')
				draw_networkx_edges(my_graph, pos)
				nx.draw(my_graph, with_labels=False, font_weight='bold', node_color=color_list)
				plt.show()
				plt.pause(0.001)
		run_index += 1