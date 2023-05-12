# Implement a data structure SetOfStacks, comprised of multiple smaller
# stacks once the previous have exceedec capacity.
#
# SetOfStacks should be able to push and pop like a regular stack.
from collections import deque


class SetOfStacks():
	def __init__(self, max_substack_height):
		self.max_substack_height = max_substack_height
		self.substacks = deque()

	def __str__(self):
		title_string = f"Substack height: {self.max_substack_height}\n"
		return title_string + "\n".join(map(lambda ss: ", ".join(ss), self.substacks))

	def push(self, item):
		if not self.substacks or len(self.substacks[-1]) == self.max_substack_height:
			self.substacks.append(deque([item]))
		elif len(self.substacks[-1]) < self.max_substack_height:
			self.substacks[-1].append(item)
		else: #should never happen
			raise Exception("Somehow one of the substacks got too big...")



	def pop(self):
		if not self.substacks: 
			return None
		top_substack = self.substacks.pop()
		top_item = top_substack.pop()
		print(f"popping..... {top_item}")
		if top_substack:
			self.substacks.append(top_substack)

s = SetOfStacks(8)
s.push('map')
s.push('big')
s.push('class')
s.push('def')
s.push('elif')
s.push('from')
s.push('got')
s.push('height')
s.push('import')
s.push('join')
s.push('k')



