# Computes x and y values necessary for the plotting of trajectories in a hasse diagramm

# The idea is to have a more abstract representation of the hasse-diagramm
# Instead of displaying every node and every edge there will simply be a 2-D
# grid where each abstraction is assigned a unique position determined by simple
# rules. This is done in order to save memory
# The y-position, as in a hasse-diagramm will be determined by the number of
# species within an abstraction
# The x-position will be determined by the lexicographical position of
# the bitstring representing the abstraction.
# In order to achieve the commonly used diamond like structure of the
# hasse-diagramm the x-positions will be centered around
# choose(number_of_species_total,number_of_species_in_abstraction) / 2

import json
import sos
import numpy
import math
import matplotlib.pyplot as plt

# Methods that are needed to calculate the position of an abstraction on the grid

def position_on_grid(a):
    if(sos.n_elements(a)==0 or sos.n_elements==len(a)):
        x=0
    else:
        b = math.comb(len(a),sos.n_elements(a)) # The breadth of the hasse-diamond at the corresponding y-position
        x = -(b/2) + sos.lexicographical_position(a)
    y = sos.n_elements(a)
    return([x,y])

def positions_on_grid(m):
    x_positions = []
    y_positions = []
    for j in range(len(m)):
        x_y_positions = position_on_grid(m[j])
        x_positions.append(x_y_positions[0])
        y_positions.append(x_y_positions[1])
    return(x_positions, y_positions)

# Two methods that will return functions that outline the hasse-diamond for better visualization

def lower_bound_diamond(n):
    x_center = 0
    y_center = n
    x_left   = []
    x_right  = []
    y_left   = []
    y_right  = []
    if n%2==0:
        y_max = int(n/2)-1
    else:
         y_max = int(n/2)
    for i in range(n-1, y_max, -1):
        y_left.append(n-i)
        y_right.append(n-i)
        breadth = math.comb(n,(n-i))
        x_left.append((-1)*breadth/2)
        x_right.append(breadth/2)
    x_left.reverse()
    y_left.reverse()
    x_left.append(0)
    y_left.append(0)
    return([x_left+x_right,y_left+y_right])

def upper_bound_diamond(n):
    x_center = 0
    n_ = n
    x_left   = []
    x_right  = []
    y_left   = []
    y_right  = []
    if n%2==0:
        y_min = int(n/2)-1
    else:
         y_min = int(n/2)
    for i in range(n-1, y_min, -1):
        y_left.append(i)
        y_right.append(i)
        breadth = math.comb(n,(n-i))
        x_left.append((-1)*breadth/2)
        x_right.append(breadth/2)
    x_left.reverse()
    y_left.reverse()
    x_left.append(0)
    y_left.append(n)
    return([x_left+x_right,y_left+y_right])

def plot_hasse(subplot, abstractions, title='', loga=False):
    '''
    In:  subplot (matplotlib.pyplot subplot)
         abstractions (list), list of binary arrays that represent the abstractions in the random walk
         change_function (function), function that calculates the distance between pairs of abstractions
        loga (boolean), logarithmic scale on x_axis (recommended for larger number of species
    '''
    
    # 1. Calculate bounderies of the hasse-diamond
    lb = lower_bound_diamond(len(abstractions[0][0]))
    ub = upper_bound_diamond(len(abstractions[0][0]))

    # 2. Plot
    subplot.plot(lb[0], lb[1], color="blue")                # Plots upper boundary of the hasse-diagram
    subplot.plot(ub[0], ub[1], color="blue")                # Plots upper boundary of the hasse-diagram
    subplot.fill_between(lb[0], lb[1] ,ub[1], color="blue") # Fill the area inbetween
    if len(abstractions)==1:
        x_p, y_p = positions_on_grid(abstractions[0])
        subplot.plot(x_p,y_p,color='red')
    for a in abstractions:
        x_p, y_p = positions_on_grid(a)
        if len(abstractions)==1:
            subplot.plot(x_p,y_p, color = 'red')
        else:
            subplot.plot(x_p,y_p)
    subplot.get_xaxis().set_visible(False)
    subplot.set_ylabel('Number of species')
    subplot.set_title(f'{title}\nTrajectory in the hasse-diagramm')
    if(loga):
        subplot.set_xscale("symlog")
