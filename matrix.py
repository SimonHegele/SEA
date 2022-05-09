# A script that provides functions to manipulate matrices

import numpy

def print_matrix(m):
    for i in range(len(m)):
        s = ""
        for j in range(len(m[0])):
            s = s + str(m[i][j]) + " "
        print(s)

def extend_columns(m, size):
    '''
    In: matrix m and int size
    Out: matrix m with additional columns whre every value is 0 
    '''
    if(isinstance(m[0],int)):
        m=[m,[0 for i in range(m.shape[0])]]
    m=numpy.array(m)
    while m.shape[1]<size:
        m=numpy.c_[m,numpy.array([0 for i in range(m.shape[0])])]
    return(m.tolist())

def uniform_ncol(rndws, x):
    # 1 Determine maximum amount of steps for the random walks
    steps = []
    i = 0
    for rndw in rndws:
        steps.append(len(rndw[x][0]))
    max_steps = max(steps)
    # 1.2 Append empty (every field is 0) columns to the matrix so that they are of equal sizes
    for rndw in rndws:
        rndw[x]=extend_columns(rndw[x],max_steps)
    return(rndws)