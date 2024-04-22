# Implement three stacks using a single array.

from collections import namedtuple

Partition = namedtuple("Partition", "start end")
class StackName:
	FIRST = 'first'
	MIDDLE = 'middle'
	LAST = 'last'

class ThreeStacks():
	def __init__(self):
		self.stacks = []
		# middle stack length is just for compatibility and sanity check, we do not use it
		self.lengths = { StackName.FIRST:0,StackName.MIDDLE: 0, StackName.LAST:0}

	def _get_stack_top(self, stack_name):
		match stack_name:
			# top of first stack is the beginning of the list
			case StackName.FIRST:
				return 0;
			# top of middle stack is the end of the first stack
			case StackName.MIDDLE:
				return self.lengths[StackName.FIRST]
			# top of last stack is n away from the end of the list (where n is the length of the last stack)
			case StackName.LAST:
				return len(self.stacks) - self.lengths[StackName.LAST] 
			case _:
				raise ValueError("u have to specify the 'first', 'middle', or 'last' stack,,,")

	def _get_stack(self, stack_name):
		match stack_name:
			# top of first stack is the beginning of the list
			case StackName.FIRST:
				return self.stacks[self._get_stack_top(StackName.FIRST):self._get_stack_top(StackName.FIRST)+self.lengths[StackName.FIRST]];
			# top of middle stack is the end of the first stack
			case StackName.MIDDLE:
				return self.stacks[self._get_stack_top(StackName.MIDDLE):self._get_stack_top(StackName.LAST)]
			# top of last stack is n away from the end of the list (where n is the length of the last stack)
			case StackName.LAST:
				return self.stacks[self._get_stack_top(StackName.LAST):self._get_stack_top(StackName.LAST)+self.lengths[StackName.LAST]]
			case _:
				raise ValueError("u have to specify the 'first', 'middle', or 'last' stack,,,")
	
	def __str__(self):
		first_stack= self._get_stack(StackName.FIRST)
		middle_stack= self._get_stack(StackName.MIDDLE)
		last_stack= self._get_stack(StackName.LAST)
		return '\n'.join(map(str, [first_stack, middle_stack, last_stack]))

	# specify which stack by 0, 1, 2
	def push(self, item, stack_name):
		self.stacks.insert(self._get_stack_top(stack_name), item)
		self.lengths[stack_name] += 1

	def pop(self, stack_name):
		# try to pop from a copy of the stack to see if a pop is possible
		self._get_stack(stack_id).pop()

		# if no error, then actually remove the value
		item = self.stacks.pop(self._get_stack_top(stack_name))
		self.lengths[stack_name] -= 1
		return item


t = ThreeStacks()
t.push('1a', StackName.FIRST)
t.push('1b', StackName.FIRST)
t.push('1c', StackName.FIRST)
t.push('1d', StackName.FIRST)
t.push('1e', StackName.FIRST)
t.push('1f', StackName.FIRST)
t.push('1g', StackName.FIRST)
t.push('1h', StackName.FIRST)
t.push('2a', StackName.MIDDLE)
t.push('2b', StackName.MIDDLE)
t.push('2c', StackName.MIDDLE)
t.push('3a', StackName.LAST)
