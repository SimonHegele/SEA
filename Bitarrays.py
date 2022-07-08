# This script helps with the computation of bitarrays

import math

# A method that simply counts the number of ones in a bitarray
def number_of_ones(bit_array):
    count = 0
    for i in range(len(bit_array)):
        if bit_array[i]==1:
            count+=1
    return count

# A method to calculate the lexicoraphic position of a bitarray 
# within the set of all bitarrays with the same length n and amount of ones
def lexicographical_position(a):
    n = len(a)
    k = number_of_ones(a)
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
    if number_of_ones(difference(a1,a2))==0:
        return True
    return False

def change_simon(a1,a2):
    na1 = complement(a1)
    na2 = complement(a2)
    if number_of_ones(union(a1,a2)) == 0 or number_of_ones(union(na1,na2)) == 0:
        return 0
    else:
        x = number_of_ones(difference(union(a1,a2),intersection(a1,a2)))/number_of_ones(union(a1,a2))
        y =  number_of_ones(difference(union(na1,na2),intersection(na1,na2)))/number_of_ones(union(na1,na2))
        return x*y
