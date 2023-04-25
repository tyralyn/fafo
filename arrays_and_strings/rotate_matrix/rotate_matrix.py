""" Given a matrix, rotate it 90 degrees clockwise.
"""

def rotate_matrix(matrix):
    """Assume matrix is provided properly, as array of arrays"""
    m=[[None for i in range(len(matrix))] for i in range(len(matrix[0]))]
    print(matrix)
    print(m)
    for i in range(len(matrix[0])):
        #row = []
        for j in range(len(matrix)):
            print(len(matrix)-j-1, i)
            m[i][j]=matrix[len(matrix)-j-1][i]
    return m

