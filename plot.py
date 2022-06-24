# Provides functions that help to design nice plots with multiple subplots

import math
import matplotlib.pyplot as plt

def dividers(n):
    dividers = []
    for i in range(1,n+1):
        if(n%i==0):
            dividers.append(i)
    return(dividers)

def dimensions(n):
    '''
    In: n (int), number of plots to be drawn
    Out: Pair (x,y) with x*y=n and x and y of similar size
    For a number n of subplots this function calculates nice
    dimensions for a plot 
    '''
    ds = dividers(n)
    y_ = math.ceil((len(ds)-1)/2)
    x_ = math.floor((len(ds)-1)/2)
    while True:
        if(ds[y_]*ds[x_]==n):
            return([ds[x_],ds[y_]])
        y_ += 1
        x_ -= 1

def initialize_subplots(n):
    '''
    In: n (int)
    Initializes and returns a plot with n subplots
    '''
    dim_x, dim_y = dimensions(n)
    figure, axes = plt.subplots(dim_x, dim_y, sharex=True, sharey=True)
    plt.tight_layout()
    return(figure, axes)

def xlabel_subplots(figure, axes, xlabel):
    '''
    Sets ylabels only for the lowest subplots in each column of a plot
    ''' 
    n_rows, n_cols = figure.axes[1].get_subplotspec().get_topmost_subplotspec().get_gridspec().get_geometry()
    for col in range(n_cols):
        print(col)
        axes[n_rows-1][col].set_xlabel(xlabel)

def ylabel_subplots(figure, axes, ylabel):
    '''
    Sets xlabels only for the most left subplots in each row of a plot
    '''
    n_rows = figure.axes[0].get_subplotspec().get_topmost_subplotspec().get_gridspec().get_geometry()[0]
    for row in range(n_rows):
        axes[row][0].set_ylabel(ylabel)
