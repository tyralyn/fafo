# Implement a queue class using two stacks.
#
# A queue is FIFO, whereas stacks are LIFO.
from collections import deque

class Queue():

	def __init__(self):
		self.left = deque()
		self.right = deque()

	def push(self, item):
		while self.right:
			self.left.append(self.right.pop())
		self.left.append(item)

	def pop(self):
		while self.left:
			self.right.append(self.left.pop())
		return self.right.pop()

	def __str__(self):
		return ", ".join(map(str, self.left + deque(reversed(self.right))))
		# returns item at top

q = Queue()
q.push(1)
q.push('b')
q.push(3)
q.push(4)