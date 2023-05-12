"""Given a matrix, if an element in the matrix is 0, set its entire row and columnn to zero.

Assume the matrix is given in proper format (array of arrays), with only integers or floats.
"""

from functools import reduce
from operator import and_

def zero_matrix(matrix):
    """make a matrix of 1/0 indicating zero or not zero for the others in its row or column.
    Then & the matrices together to determine whether it's itself or zero
    """
    comp_m = [[None for item in matrix[0]] for item in matrix]
    for column in range(len(matrix[0])):
        for row in range(len(matrix)):
            zero_in_row = 0 not in matrix[row]
            zero_in_column = 0 not in [matrix[i][column] for i in range(len(matrix))]
            comp_m[row][column]=zero_in_row & zero_in_column
    print (comp_m)
    return [[int(comp_m[j][i]) * matrix[j][i] for i in range(len(matrix[0]))] for j in range (len(matrix))]
