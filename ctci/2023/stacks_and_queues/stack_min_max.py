# Design a stack that also can retrieve the min and max (and push and pop) in O(1) time.

from collections import namedtuple
from random import randint

Item = namedtuple("Item", "value current_min current_max")

class MinMaxStack():
	def __init__(self):
		self.stack = []

	# when pushing, compare item to top of stack to get min and max, and save
	def push(self, item):
		min_item = item if not self.stack else min(item, self.stack[-1].current_min)
		max_item = item if not self.stack else max(item, self.stack[-1].current_max)
		self.stack.append(Item(item, min_item, max_item))

	def pop(self):
		return self.stack.pop()

	def min(self):
		return self.stack[-1].current_min

	def max(self):
		return self.stack[-1].current_max

	def __str__(self):
		items = [f"{item.value} (min: {item.current_min}, max: {item.current_max})" for item in self.stack]
		return "\n".join(items)

mms = MinMaxStack()

[mms.push(randint(-100, 100)) for i in range(25)]