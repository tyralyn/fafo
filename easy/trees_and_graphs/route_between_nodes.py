# basic impls of DFS and BFS for connected graphs, printing the items
from random import randint
from collections import deque

nodes = []

class Node:
	def __init__(self, id, value=None):
		self.id = id
		self.value=value
		self.adjacencies = set()
		self.touched = [False, False]

	def __str__(self):
		touched_str = str(self.touched)
		return f"{self.id}: {self.value} ({touched_str}) [{', '.join(map(str, [node.id for node in self.adjacencies]))}])"

	def add_adjacencies(self, nodes):
		self.adjacencies |= nodes

def untouch(node):
	print(f"untouching node {node.id}")
	node.touched=False

def sample_graph():
	global nodes
	nodes = [Node(i) for i in range(6)]
	nodes[0].add_adjacencies({nodes[1], nodes[4], nodes[5]})
	nodes[1].add_adjacencies({nodes[4], nodes[3]})
	nodes[2].add_adjacencies({nodes[1]})
	nodes[3].add_adjacencies({nodes[2], nodes[4]})
	
	return(nodes[0])

def breadth_first(node, visit_func=print):
	queue = deque([node])
	while queue:
		current_queue_str = ", ".join(map(lambda item: str(item.id), queue))
		node = queue.popleft()

		if not node.touched[0]:
			visit_func(node)
			node.touched[0] = True

		for adj in node.adjacencies:
			if not adj.touched[0]:
				queue.append(adj)
				#adj.touched = True

def connected(node0, node1):# , visit_func=print):
	queue0 = deque([node0])
	queue1 = deque([node1])

	while queue0 or queue1:
		queue0_str = ", ".join(map(lambda item: str(item.id), queue0))
		queue1_str = ", ".join(map(lambda item: str(item.id), queue1))
		#current_queue_str = ", ".join(map(lambda item: str(item.id), queue0))
		##print("end of loop..." + str(n0) + " queue:" + current_queue_str)
		#print("-----------")
		#print(f"queue0: ({queue0_str})")
		#print(f"queue1: ({queue1_str})")


		if queue0:
			n0 = queue0.popleft()
			#print(f"popped out node ({n0}) out of queue0")
			if not n0.touched[0]:
				#visit_func(n0)
				n0.touched[0]=True
			if n0.touched[1]:
				return True
			for adj in n0.adjacencies:
				if not adj.touched[0]:
					queue0.append(adj)
			#print(f"    at end of popping, node is ({n0})")

		if queue1:
			n1 = queue1.popleft()
			#print(f"popped out node ({n1}) out of queue1")
			if not n1.touched[1]:
				#visit_func(n1)
				n0.touched[1]=True
			if n1.touched[0]:
				return True

			for adj in n1.adjacencies:
				if not adj.touched[1]:
					queue1.append(adj)
			#print(f"    at end of popping, node is ({n1})")
		#print("-----------")
	return False



g=sample_graph()
print(connected(nodes[3], nodes[2]))
