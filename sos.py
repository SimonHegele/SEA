################################
# SOS - set operations service #
################################

'''
This library provides various set operations and related functions.

For a fixed set S={x1,...xn} each subsets S' is represented by a list L,
where L[i]=1 if xi ∈ S' and L[i]=0 else. 
'''

import math
import copy

def from_string(string):
    '''
    In:  string (string)
    Out: list   (list)
    Converts a string like '[1,0,1,0]'
    This is needed because pandas dataframe cannot store lists
    '''
    return [int(i) for i in string[1:len(string)-1].split(',')]

def create(length, indices):
    '''
    In:  length (int)
         indices (list)
    Out: A bitarray where a[i]=1 if i in indices and a[i]=0 else
    '''
    a = [0 for i in range(length)]
    for i in indices:
        a[i]=1
    return a

def toString(a):
    s = ""
    for e in a:
        s = s + str(e)
    return s

def dec_to_bit(d, n):
    '''
    In:  d (int)
         n (int)
    Out: binary representation of d in a bitarray of length n
    '''
    b = [0 for i in range(n)]
    for i in range(n):
        if d == 0:
            break
        v = 2**(n-i-1)
        if(d >= v):
            b[i] = 1
            d = d-v
    return b

def bit_to_dec(a):
    d = 0
    a.reverse()
    for i in range(len(a)):
        d = d+a[i]*(2**i)
    return d

def generate_all(n):
    '''
    In:  n
    Out: A list of all bitarrays of length n
    '''
    return [dec_to_bit(i,n) for i in range(2**n)]

# A method that simply counts the number of ones in a bitarray
def n_elements(bit_array):
    count = 0
    for i in range(len(bit_array)):
        if bit_array[i]==1:
            count+=1
    return count

def add_bit(a):
    a = copy.copy(a)
    for i in reversed(range(len(a))):
        if a[i]==0:
            a[i]=1
            return a
        else:
            a[i]=0
    return a

# A method to calculate the lexicoraphic position of a bitarray 
# within the set of all bitarrays with the same length n and amount of ones
def lexicographical_position(a):
    n = len(a)
    k = n_elements(a)
    lex_pos=0
    for i in range(n):
        if a[i] == 1:
            lex_pos += math.comb(n-1,k)
            n -= 1
            k -= 1
        else:
            n -= 1
            if(k==n):
                break
    return(lex_pos)

# Some set operations

def complement(a):
    return [(lambda x: 1 if (x==0) else 0)(a[i]) for i in range(len(a))]

def union(a1,a2):
    return [(lambda x,y: 1 if (x==1 or y==1) else 0)(a1[i],a2[i]) for i in range(len(a1))]

def intersection(a1,a2):
    return [(lambda x,y: 1 if (x==1 and y==1) else 0)(a1[i],a2[i]) for i in range(len(a1))]

def difference(a1,a2):
    return [(lambda x,y: 1 if (x==1 and y==0) else 0)(a1[i],a2[i]) for i in range(len(a1))]

def is_subset_of(a1,a2):
    if n_elements(difference(a1,a2))==0:
        return True
    return False

def cs(a1, a2):
    if n_elements(union(a1,a2)) == 0:
        return 0
    return n_elements(difference(union(a1,a2),intersection(a1,a2)))/n_elements(union(a1,a2))

def change_global(a1,a2):
    return cs(a1,a2)*cs(complement(a1),complement(a2))

def change_local(a1,a2):
    if n_elements(union(a1,a2)) == 0:
        return 0
    return 1-(n_elements(intersection(a1,a2))/n_elements(union(a1,a2)))

def change_max_based(a1,a2):
    if n_elements(union(a1,a2)) == 0:
        return 0
    return(max(n_elements(difference(a1,a2)),n_elements(difference(a2,a1)))/max(n_elements(a1),n_elements(a2)))

def changes(formula, n):
    '''
    In: formula, function that is used to calculate the change
        n, number of species
    Out: Matrix with the change between every pair of abstractions
    '''
    lst = [[0 for i in range(n)]]
    for i in range(2**n-1):
        lst.append(add_bit(lst[i]))
    lst.sort(key=n_elements)
    return [[formula(lst[j],lst[i])**2 for j in range(len(lst))] for i in range(len(lst))]

def sort(list):
    '''
    Sorts a list of bitarrays first by lexicographical order and then by number of ones
    '''
    all = generate_all(len(list[0])).sort(key=n_elements)
    sorted_list = []
    for e1 in all:
        for e2 in list:
            if e1 == e2:
                sorted_list.append(e1)
    return(sorted_list)