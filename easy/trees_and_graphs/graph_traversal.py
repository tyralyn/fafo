# basic impls of DFS and BFS for connected graphs, printing the items
from random import randint
from collections import deque

class Node:
	def __init__(self, id, value=None):
		self.id = id
		self.value=value
		self.adjacencies = set()
		self.touched = False

	def __str__(self):
		touched_str = "touched" if self.touched else "untouched"
		return f"{self.id}: {self.value} ({touched_str}) [{', '.join(map(str, [node.id for node in self.adjacencies]))}])"

	def add_adjacency(self, node):
		self.adjacencies.add(node)

	def add_adjacencies(self, nodes):
		self.adjacencies |= nodes

def depth_first(node, visit_func=print):
	if not node: 
		return

	visit_func(node)
	node.touched = True

	for n in node.adjacencies:
		if not n.touched:
			depth_first(n)

def breadth_first(node, visit_func=print):
	queue = deque([node])
	while queue:
		current_queue_str = ", ".join(map(lambda item: str(item.id), queue))
		node = queue.popleft()

		if not node.touched:
			visit_func(node)
			node.touched = True

		for adj in node.adjacencies:
			if not adj.touched:
				queue.append(adj)
				#adj.touched = True

class ConnectedGraph():

	def __init__(self, node=None):
		if node:
			self.node = node
		else:
			nodes = [Node(i) for i in range(6)]
			nodes[0].add_adjacencies({nodes[1], nodes[4], nodes[5]})
			nodes[1].add_adjacencies({nodes[4], nodes[3]})
			nodes[2].add_adjacencies({nodes[1]})
			nodes[3].add_adjacencies({nodes[2], nodes[4]})
			self.node=nodes[0]

	def __str__(self):
		# this goes breadth first bc the depth first as is cant return and update a list
		# by passing in a lambda.... i think recursion is the problem...
		bf = []
		breadth_first(self.node, lambda x: bf.append(x.id))
		return ", ".join(map(str, bf))

	def BF(self):
		breadth_first(g.node)

	def DF(self):
		depth_first(g.node)


	#def shortest_path(self, src_node, dest_node):


g = ConnectedGraph()

# g.BF() or g.DF(), and then g.reset() after
# to print basic info on a node's adj's adj
# [print(adj) for adj in g.adjacencies]



