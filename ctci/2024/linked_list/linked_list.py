from node import *

class LinkedList:

	def __init__(self, node_values=None):
		# set head to none
		self.head=None
		# check for node_values list
		if node_values is not None and node_values:
			# remove the first item from the node_values list, make a node out of it
			# variable node is a temp, like referring to a node
			node = Node(data=node_values.pop(0))
			# set head to a node made out of the first item of the list 
			self.head = node
			# iterate through the remaining node values
			for item in node_values:
				# set the temp's next value
				node.next = Node(item)
				# move the temp variable to the next thing
				node = node.next


	def __repr__(self):
		# refer to the top of the linked list, head
		n = self.head
		node_data = []
		# iterating through the remaining nodes in the list
		while n.next is not None:
			node_data.append(n.data)
			n = n.next
		node_data.append(n.data)
		return " --> ".join(map(str, node_data))

	def insert(self, n:Node):
		hold = self.head
		self.head=n
		n.next = hold


l=LinkedList(node_values=['a', 33, False])
#print(l)
l.insert(Node('ffffffff'))
#print(l)

