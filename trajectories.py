# This script plots the trajectories for a given set of evolutions

import hasse
import plot
import numpy
import bitarrays
import matrix
import matplotlib.pyplot as plt

def x_(x):
    if x ==  "a":
        return "present species"
    return "active species"

def plot_raw(rndws, x):
    '''
    In: rndws (list), list of random walks
        x (string), "a" to plot abstractions of present species
                    "u" to plot abstractions of active species
    '''

    # 1. Set up subplots
    figure, axes = plot.initialize_subplots(len(rndws))
    plot.xlabel_subplots(figure, axes, 'steps in random walk')
    plot.ylabel_subplots(figure, axes, 'Species index')
    
    # 2. Set the matrices of the random walks to an equal length
    rndws = matrix.uniform_ncol(rndws, x)

    #3. Plot
    for index, subplot in enumerate(figure.axes):
        subplot.imshow(rndws[index][x],vmin=0, vmax=1)
    figure.suptitle(f"Trajectory of abstractions ({x_(x)})")

def abstraction_sizes(rndws, x):
    '''
    In: rndws (list), list of random walks
        x (string), "a" to plot abstractions of present species
                    "u" to plot abstractions of active species
    '''

    # 1. Set up subplots
    figure, axes = plot.initialize_subplots(len(rndws))
    plot.xlabel_subplots(figure, axes, 'abstraction size')
    plot.ylabel_subplots(figure, axes, 'observations')

    #2. Plot
    for index, subplot in enumerate(figure.axes):
        m = numpy.transpose(rndws[index][x])
        n_species = len(rndws[index][x])
        xp = [x for x in range(n_species+1)]
        yp = [0 for x in range(n_species+1)]
        # Count observations
        for j in range(len(m)):
            yp[bitarrays.number_of_ones(m[j])] += 1
        subplot.bar(xp, yp)
    figure.suptitle(f"Size of abstractions ({x_(x)})")

def plot_hasse(rndws, x, loga=False):
    '''
    In: rndws (list), list of random walks
        x (string), "a" to plot abstractions of present species
                    "u" to plot abstractions of active species
        loga (boolean), logarithmic scale on x_axis (recommended for larger number of species
    '''
    
    # 1. Set up subplots
    figure, axes = plot.initialize_subplots(len(rndws))
    plot.xlabel_subplots(figure, axes, 'abstraction size')
    plot.ylabel_subplots(figure, axes, 'observations')

    # 2. Calculate bounderies of the hasse-diamond
    lb = hasse.lower_bound_diamond(len(rndws[0][x]))
    ub = hasse.upper_bound_diamond(len(rndws[0][x]))

    # 2. Plot
    for index, subplot in enumerate(figure.axes):
        x_, y_ = hasse.positions_on_grid(rndws[index], x)
        subplot.plot(lb[0], lb[1], color="blue")            # Plots upper boundary of the hasse-diagram
        subplot.plot(ub[0], ub[1], color="blue")            # Plots upper boundary of the hasse-diagram
        subplot.fill_between(lb[0], lb[1] ,ub[1])           # Fill the area inbetween
        subplot.plot(x_,y_,color="red")
        subplot.get_xaxis().set_visible(False)              #Plots tracectory
    if(loga):
        plt.xscale("symlog")
    figure.suptitle(f"Trajectory of abstractions in hasse_diagram ({x_(x)})")
