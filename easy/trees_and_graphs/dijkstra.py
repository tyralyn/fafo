# sample implementation of dijkstras algo for shortest path
# for undirected graph

from collections import namedtuple, deque, defaultdict
import random

Path = namedtuple("Path", "node weight")


# (v1, v2, weight)
SAMPLE_GRAPH_PAIRS = [
	(0, 1, 2),
	(1, 3, 5),
	(2, 3, 8),
	(0, 2, 6),
	(3, 5, 15),
	(5, 6, 6),
	(4, 6, 2),
	(3, 4, 10),
	(4, 5, 6)
]


class Node():
	def __init__(self, id):
		self.id = id
		self.adjacencies = set()
		self.touched = False

	def __str__(self):
		touched_str = "touched" if self.touched else "untouched"
		return f"{self.id} ({touched_str}) [{', '.join(map(str, [adj.node.id for adj in self.adjacencies]))}])"

	def add_adjacency(self, adj):
		self.adjacencies.add(adj)

	def add_adjacencies(self, adjs):
		self.adjacencies |= adjs


def sample_graph():
	# turn tuples into a dict adj list
	v1s, v2s, weights = zip(*SAMPLE_GRAPH_PAIRS)

	# for each vertex, make a node
	nodes = { v: Node(v) for v in set(v1s+v2s)}
	#print(nodes)s

	for v1,v2,weight in SAMPLE_GRAPH_PAIRS:
		# since this is an undirected graph add edge to both vertices
		#print(f"-- {nodes[v1]}, {nodes[v2]} --")
		nodes[v1].add_adjacency(Path(nodes[v2], weight))
		nodes[v2].add_adjacency(Path(nodes[v1], weight))

	# return one of the nodes idk which
	return random.choice(nodes)


def breadth_first(node, visit_func=print):
	queue = deque([node])
	while queue:
		current_queue_str = ", ".join(map(lambda item: str(item.id), queue))
		node = queue.popleft()

		if not node.touched:
			visit_func(node)
			node.touched = True

		for adj in node.adjacencies:
			if not adj.node.touched:
				queue.append(adj.node)
				#adj.touched = True

def print_graph():
	global g
	breadth_first(g)
	g = sample_graph()


# dijkstra is breadth first
def dijkstra_traversal(node):
	queue = deque([Path(node, 0)])
	# key: node, value: (distance from origin node, backpath node)
	shortest_paths = defaultdict(set)
	shortest_paths[node] = (float('inf'), None)

	while (queue):
		current_queue_str = ", ".join(map(lambda item: str(item.node.id), queue))
		adj = queue.popleft()
		print(f"---- {str(adj.node)}")
		print(f"queue: {current_queue_str}")
		
		if not adj.node.touched:
			if adj.node not in shortest_paths.keys():
				shortest_paths[adj.node]=(adj.weight, [adj.node])
			#else:


			adj.node.touched = True

		for adj in adj.node.adjacencies:
			if not adj.node.touched:
				queue.append(adj)


g = sample_graph()





