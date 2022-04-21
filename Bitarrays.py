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