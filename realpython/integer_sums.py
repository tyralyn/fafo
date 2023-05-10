# Write a function that takes a single integer as input
# and returns the sum of integers from zero to the input parameter
# (returns zero of a non-integer is passed in)
#
# inputs: single input (not necessarily an integer)
# output: sum of integers
# 
# Q: regarding checking the input, would a string representation
# of an integer work? e.g. "-9"
# A: yes
#
# Q: is this inclusive?
# A: yes

def integer_sum_basic(number):
	try:
		n=int(number)
	except ValueError:
		return 0 
	total = 0
	for i in range (number, 0, -int(number/abs(number))):
		total += i
	return total



# using the sum method
def integer_sum(number):
	try:
		n=int(number)
	except ValueError:
		return 0 
	return sum(range (number, 0, -int(number/abs(number))))