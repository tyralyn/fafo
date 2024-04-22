from linked_list import *

def remove_dups(ll):
	"""this will remove all but the last instances of each duplicate."""
	data_hold = []
	for node in ll:
		if node.data not in data_hold:
			data_hold.append(node.data)
		else:
			ll.remove_node(node.data)
	return ll

def remove_dups_no_buffer(ll):
	n1 = ll.head
	while n1 is not None:
		prev_node=n1
		n2 = n1.next
		while n2 is not None:
			if (n1.data == n2.data):
				# delete the node referred to by the current pointer
				prev_node.next = n2.next
			else:
				prev_node = n2
			n2 = n2.next
		n1 = n1.next




l=LinkedList(nodes=['a', 'b', 'b', 'd', 'b', 'b'])