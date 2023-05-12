# implement n stacks in one array
import string

class ManyStacks():
	def __init__(self, n):
		self.n=n
		self.stacks = []
		self.lengths = [0] * n

	def _is_stack_valid(self, stack_id):
		try:
			n=int(number)
		except ValueError:
			print("input has to be an int u dumbo")
		if stack_id_num < 0 or stack_id_num >= len(self.n):
			print(f"input has to be between 0 and {len(self.n)-1}")

	def _get_top(self, stack_id):
		# 0: 0
		# 1: len(0)
		# 2: len(0) + len(1)
		# ...
		if stack_id == 0:
			return 0
		return sum(self.lengths[0:stack_id])

	def _get_stack(self, stack_id):

		return self.stacks[self._get_top(stack_id):self._get_top(stack_id) + self.lengths[stack_id]]


	# specify which stack by 0, 1, 2
	def push(self, item, stack_id):
		self.stacks.insert(self._get_top(stack_id), item)
		self.lengths[stack_id] += 1

	def pop(self, stack_id):
		# is popping from that stack even possible?
		self._get_stack(stack_id).pop()

		# if so, actually pop the item out
		item = self.stacks.pop(self._get_top(stack_id))
		self.lengths[stack_id] -= 1
		return item

	def __str__(self):
		title = f"There are {self.n} stacks.\n"
		return title + '\n'.join(map(str, map(self._get_stack, range(self.n))))

m = ManyStacks(4)

# sample inputs -- push a bunch of chars
list(map(lambda c: m.push(c, 0), string.ascii_lowercase[:5]))
list(map(lambda c: m.push(c, 1), string.ascii_lowercase[14:17:]))
list(map(lambda c: m.push(c, 2), string.ascii_lowercase[:2]))
list(map(lambda c: m.push(c, 3), string.ascii_lowercase))
