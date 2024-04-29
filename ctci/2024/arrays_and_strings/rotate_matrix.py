# Given an image represented by an N x N matrix, where each pixel in the image is represented by an integer, write a method to rotate the image by 90 degress
# clockwise?
#
# Can you do this in place?
#
# sample input ---> output
# 2,3,4    ----->    8,5,2
# 5,6,7    ----->    9,6,3
# 8,9,0    ----->    0,7,4
#
# sample input --> output
# 81, 82, 83, 84    ----->    91, 10, 11, 81
# 11, 22, 33, 44    ----->    92, 20, 22, 82
# 10, 20, 30, 40    ----->    93, 30, 33, 83
# 91, 92, 93, 94    ----->    94, 40, 44, 84
#
# (0,0) --> (0, dim) 
# (0,1) --> (1, dim)
# (dim, 0) --> (0, 0)
# (dim, 1) --> ()
# (1, 2) --> () 
#
# TODO: do we need to validate all input as integers?

def rotateMatrix(m:list[list[int]]):
	dim = len(m)
	# check for square:
	if len(list(filter(lambda row: len(row)!= dim, m))) != 0:
		return None

	result = [[None for x in range(dim)] for y in range(dim)]
	for row in range(dim):
		for col in range(dim):
			result[col][dim-1-row] = m[row][col]
	return result

m = [[81, 82, 83, 84], [11, 22, 33, 44], [10, 20, 30, 40], [91, 92, 93, 94]]

print(rotateMatrix(m))