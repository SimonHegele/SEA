# A script that calculates and vizualizes the probabilities for every species to  be observed at any given time step.
# The probability that a species i is present at time t is  defined as 
# the fraction of random walks where species i is present at time t
# This is of course not really the probability but rather an estimate of it)

import numpy
import math
import matrix
import matplotlib.pyplot as plt
import time

def global_ops(rndws, x):
    '''
    In: list of random walks as dictionaries,
        identifier x "a" or "u"
    Out: A matrix with the the occurrence probabilities for every species at any time
    For a species i and time t the occurrence probability is estimated by the fraction 
    of random walks where i is present at time t 
    '''
    # 1. Equal sizes for the matrix
    # 1.1 Determine maximum amount of steps for thr randomwals
    steps = []
    i = 0
    for rndw in rndws:
        steps.append(len(rndw[x][0]))
    max_steps = max(steps)
    # 1.2 Append empty (every field is 0) columns to the matrix so that they are of equal sizes
    for rndw in rndws:
        rndw[x]=matrix.extend_columns(rndw[x],max_steps)
    # 2. Count overall occurrences by matrix addition
    occurrences = numpy.array(rndws[0][x])
    for i  in range(1,len(rndws)):
        occurrences = numpy.add(occurrences, numpy.array(rndws[i][x]))
    return(occurrences/len(rndws))

def plot_ops(occurrence_probabilities):
    x = range(len(occurrence_probabilities))
    y = range(len(occurrence_probabilities[0]))
    fig, ax= plt.subplots(1,1)
    cp = ax.imshow(occurrence_probabilities, vmin=0, vmax=1)
    fig.colorbar(cp) # Add a colorbar to a plot
    ax.set_title('Occurrence probabilities for individual species')
    ax.set_ylabel('Species index')
    ax.set_xlabel('step in random walk')
    plt.tight_layout ()

def local_ops(rndw, x):
    '''
    In: a random walks as dictionaries,
        identifier x "a" or "u"
    Out: A matrix with the the occurrence probabilities for every species at any time
    For a species i and time t the occurrence probability is estimated by the fraction 
    of time steps 1,...,t where i is present
    '''
    c = [[0 for j in range(len(rndw[x][0]))] for i in range(len(rndw[x]))]
    for i in range(len(rndw[x])):
        c[i][0] = rndw[x][i][0]
        for j in range(1,len(rndw[x][0])):
            c[i][j] = c[i][j-1]
            if(rndw[x][i][j]==1):
                c[i][j] += 1
    for i in range(len(rndw[x])):
        for j in range(1,len(rndw[x][0])):
            c[i][j] = c[i][j]/len(rndw[x][0])
    return c

def averaged_local_ops(rndws, x):
    a = numpy.array(local_ops(rndws[0],x))
    for i in range(1, len(rndws)):
        a = numpy.add(a, local_ops(rndws[i], x))
    a = a/len(rndws)
    return(a)

def plot_local_ops(rndws, x):
    start = time.time()
    # 1. Equal sizes for the matrix
    rndws = matrix.uniform_ncol(rndws, x)
    # 2. Plot
    # 2.1 local occurrrence probilities
    fig, ax = plt.subplots(2, int(len(rndws)/2)+1)
    fig.suptitle("Occurrence probabilities for individual species")
    for i in range(len(rndws)):
        ax[i%2][int(i/2)].imshow(local_ops(rndws[i],x), vmin=0, vmax=1) #
        ax[i%2][int(i/2)].set_title(str(i))
        ax[i%2][int(i/2)].set_xlabel('Iteration')
        ax[i%2][int(i/2)].locator_params(axis="both", integer=True, tight=True)
    # 2.2 average local occurrence probability
    if(len(rndws)%2==0):
        ax[0][int(len(rndws)/2)].set_visible(False)
    a = averaged_local_ops(rndws, x)
    cp = ax[1][int(len(rndws)/2)].imshow(a, vmin=0, vmax=1)
    ax[1][int(len(rndws)/2)].set_title("Average")
    ax[1][int(len(rndws)/2)].set_xlabel('Iteration')
    # 2.3 Plot details
    ax[0][0].set_ylabel('Species index')
    ax[1][0].set_ylabel('Species index')
    ax[1][int(len(rndws)/2)].locator_params(axis="both", integer=True, tight=True)
    print("Preparing local-probability-plots: " + str(round(time.time()-start,4)) + "seconds")
    plt.tight_layout()
    