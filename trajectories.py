# This script plots the trajectories for a given set of evolutions

import numpy
import Bitarrays
import matrix
import math
import matplotlib.pyplot as plt
import time

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

def position_on_grid(a):
    if(Bitarrays.number_of_ones(a)==0 or Bitarrays.number_of_ones(a)==len(a)):
        x=0
    else:
        b = math.comb(len(a),Bitarrays.number_of_ones(a)) # The breadth of the hasse-diamond at the corresponding y-position
        x = -(b/2) + Bitarrays.lexicographical_position(a)
    y = Bitarrays.number_of_ones(a)
    return([x,y])

def plot_hasse(rndws, x, loga=False):
    start = time.time()
    figure, axis = plt.subplots(2,math.ceil(len(rndws)/2), sharex=True) # Two rows of plots
    figure.suptitle("Random walks in the hasse-diagram")
    # calculate hasse-diamond
    lb = lower_bound_diamond(len(rndws[0][x]))
    ub = upper_bound_diamond(len(rndws[0][x]))
    for i in range(len(rndws)): # one plot per random walk
        m = numpy.transpose(rndws[i][x])
        x_positions = []
        y_positions = []
        for j in range(len(m)):
            x_y_positions = position_on_grid(m[j])
            x_positions.append(x_y_positions[0])
            y_positions.append(x_y_positions[1])
        axis[i%2][int(i/2)].plot(lb[0], lb[1], color="blue")
        axis[i%2][int(i/2)].plot(ub[0], ub[1], color="blue")
        axis[i%2][int(i/2)].fill_between(lb[0], lb[1] ,ub[1])
        axis[i%2][int(i/2)].plot(x_positions,y_positions,color="red")
        axis[i%2][int(i/2)].get_xaxis().set_visible(False)
    if(loga):
        plt.xscale("symlog")
    print("Preparing hasse-plots: " + str(round(time.time()-start,4)) + "seconds")
    plt.tight_layout()

def plot_raw(rndws, x):
    # 1. Equal sizes for the matrix
    rndws = matrix.uniform_ncol(rndws, x)
    figure, ax = plt.subplots(2,math.ceil(len(rndws)/2)) # Two rows of plots
    for i in range(len(rndws)): # one plot per random walk
        ax[i%2][int(i/2)].imshow(rndws[i][x],vmin=0, vmax=1)
        ax[i%2][int(i/2)].set_xlabel('iteration')
    ax[0][0].set_ylabel('Species index')
    ax[1][0].set_ylabel('Species index')
    plt.tight_layout()