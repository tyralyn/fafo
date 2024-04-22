# an animal shelter operates in FIFO and only has cats and dogs
#
# make data structur so that someone can dequeueAny, dequeueCat, dequeueDog

from collections import deque, namedtuple

class Species():
	CAT = "cat"
	DOG = "dog"

Animal = namedtuple("Animal", "name, species")

class AnimalQueue():
	def __init__(self):
		self.animals = deque()

	def __str__(self):
		return "\n".join([f"{a.name} ({a.species})" for a in self.animals])

	def push(self, name, species):
		self.animals.append(Animal(name, species))

	def pop(self):
		return self.animals.popleft()

	'''
	def find_first_animal(self, species):
		for animal in self.animals:
			if animal.species ==
			'''

	def dequeue_species(self, species):
		first_of_species = deque([a for a in self.animals if a.species == species]).popleft()
		#filter(lambda a: for a.species == species, self.animals)
		self.animals.remove(first_of_species)
		return first_of_species

	def dequeue_any(self):
		return self.pop()

aq = AnimalQueue()

aq.push("jonesy", "cat")
aq.push("max", "dog")
aq.push("sheba", "dog")
aq.push("razbery", "cat")
aq.push("russell", "cat")
aq.push("khalifa", "cat")
aq.push("slider", "dog")
aq.push("gigi", "dog")
