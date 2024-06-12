from linked_list import LinkedList

l=LinkedList(node_values=['a', 33, False, 'a', 666, True, True, 'a', 666])

def removeDups(l):
	s=set()
	prev = None
	cur = l.head
	while cur is not None:
		print(f'{cur.data} : -- {cur.data in s} -- : {s}')
		if cur.data in s:
			prev.next = cur.next
		else:
			s.add(cur.data)
		prev = cur
		cur = cur.next
		print(f'    -------    {l}')
	return l

l=LinkedList(node_values=['a', 33, False, 'a', 666, True, True, 'a', 'a',  666, False])
# print(l)
# print(removeDups(l))
removeDups(l)