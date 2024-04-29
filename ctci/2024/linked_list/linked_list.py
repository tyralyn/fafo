from node import *

class LinkedList:

	def __init__(self, node_values=None):
		self.head=None
		if node_values is not None and node_values:
			node = Node(data=node_values.pop(0))
			self.head = node
			for item in node_values:
				node.next = Node(item)
				node = node.next


	def __repr__(self):
		n = self.head
		while n.next is not None:
			print(n.data)
			n = n.next

	def append(self, n:Node):
		hold = self.head
		self.head=n
		n.next = hold

l=LinkedList(nodes=['a', 33, False])

