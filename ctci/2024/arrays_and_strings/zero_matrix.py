# Write an algorithm such that if an element in an M x N matrix is 0, the entire row and column are set to zero
# 
# not assumed square
# am assuming correct input for now, e.g. lets assume that we are always given a matrix of size  M x N properly

import copy

def zeroMatrix(m: list[list[int]]):
	M = len(m)
	N = len(m[0]) # assuming that the all rows have the same length

	result = copy.copy(m)
	cols_with_zero = set()
	rows_with_zero = set()

	for i in range(M):
		for j in range(N):
			if m[i][j] == 0:
				cols_with_zero.add(j)
				rows_with_zero.add(i)

	for i in range(M):
		for j in range(N):
			if j in cols_with_zero:
				result[i][j] = 0
		if i in rows_with_zero:
			result[i]=[0]*N



	return result


m1= [[81, 82, 83, 84], [11, 22, 33, 44], [10, 20, 30, 40], [91, 92, 93, 94]]
print(zeroMatrix(m1))

m2 = [[81, 82, 0, 84], [11, 22, 33, 44], [10, 20, 30, 40], [0, 92, 93, 94]]
print(zeroMatrix(m2))