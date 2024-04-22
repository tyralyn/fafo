# sort a stack so that the smallest items r on top
# u can use one temp stack but no other data structures

#
# stack should be able to push, pop, peek, and isempty

from random import randint

class SortStack():
	def __init__(self):
		self.stack=[]

	def __str__(self):
		return ", ".join(map(str, self.stack))

	def sort(self):
		temp_stack = []
		while self.stack:
			temp_stack.append(self.stack.pop(self.stack.index(max(self.stack))))
		self.stack = temp_stack

	def push(self, item):
		self.stack.append(item)
		
	def pop(self):
		return self.stack.pop()
		
	def peek(self):
		return self.stack[-1]

	def isempty(self):
		return self.stack

ss = SortStack()
[ss.push(randint(-100, 100)) for i in range(24)]
		