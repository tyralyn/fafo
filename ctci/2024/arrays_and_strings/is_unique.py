# Implement an algorithm to determine if a string has all unique characters
#
# What if you can't use additional data structures?
#
# input:  "green bay packers"
# output: False
#
# input: "abc"
# output: Trues

from collections import Counter
from functools import reduce

def isUnique(s):
	counts = Counter(s).values()
	return reduce(lambda a,b: (a and b==1), counts)

print(isUnique("green bay packers"))
print(isUnique("abcdA"))


