import matplotlib.pyplot as plt
import sos

def change_plot(subplot, abstractions, change_function=sos.change_global, show_indices=True):
    '''
    In:  subplot (matplotlib.pyplot subplot)
         abstractions (list), list of binary arrays that represent the abstractions in the random walk
         change_function (function), function that calculates the distance between pairs of abstractions
    '''

    # Calculating the size of the sets before and after transitions
    x       = [sos.n_elements(abstractions[i]) for i in range(len(abstractions)-1)]
    y       = [sos.n_elements(abstractions[i+1]) for i in range(len(abstractions)-1)]

    # Plotting a diagonale to indicate numerical stability
    min_size = min([sos.n_elements(a) for a in abstractions])
    max_size = max([sos.n_elements(a) for a in abstractions])
    subplot.plot([min_size-1,max_size+1],[min_size-1,max_size+1],color ='black', label ='numerical stability')

    # Divide transitions to smaller lists by the magnitude of the change
    changes    = [change_function(abstractions[i],abstractions[i+1]) for i in range(len(x))]
    max_change = max(changes)
    small      = [(x[i],y[i],changes[i]*500*(max_size-min_size)/max_change) for i in range(len(x)) if (max_change/3)>changes[i]]
    medium     = [(x[i],y[i],changes[i]*500*(max_size-min_size)/max_change) for i in range(len(x)) if (max_change/3)<changes[i]<(2*max_change/3)]
    big        = [(x[i],y[i],changes[i]*500*(max_size-min_size)/max_change) for i in range(len(x)) if                changes[i]>(2*max_change/3)]

    # Plotting transition points
    subplot.scatter([s[0] for s in small] , [s[1] for s in small] , s=[s[2] for s in small] , color = 'green')
    subplot.scatter([m[0] for m in medium], [m[1] for m in medium], s=[m[2] for m in medium], color = 'yellow')
    subplot.scatter([b[0] for b in big]   , [b[1] for b in big]   , s=[b[2] for b in big]   , color = 'red')
    subplot.scatter([],[],s=30, label=f'small change (change < {round((max_change/3),3)})', color = 'green')
    subplot.scatter([],[],s=30, label=f'medium change ({round((max_change/3),3)} < change < {round((2*max_change/3),3)})', color = 'yellow')
    subplot.scatter([],[],s=30, label=f'big change ({round((2*max_change/3),3)} < change)', color = 'red')

    # Plotting connections
    subplot.plot(x,y)

    # Add numbers to identify order the of transitions in a way that numbers do not overlap and also add labels with the change in that transition
    if show_indices:
        x_      = [0 for xi in x]
        y_      = [0 for yi in y]
        dist    = 0.025*(max_size-min_size)
        for i in range(len(x)):                 # Iterate over all coordinates
            occurrences = 0                     # Number of previous transitions with the same coordinates
            for j in range(i):
                if x[i]==x[j] and y[i]==y[j]:
                    occurrences += 1
            if x[i]<y[i]:
                x_[i] = x[i]-dist*(occurrences+1)
                y_[i] = y[i]+dist*(occurrences+1)
            else:
                x_[i] = x[i]+dist*(occurrences+1)
                y_[i] = y[i]-dist*(occurrences+1)   
        for i in range(len(x_)):
            subplot.text(x_[i],y_[i],f'{i}', fontsize = 10, color='black')

    subplot.text(max_size-2,min_size+1, 'contraction', fontsize = 20, color='orange')
    subplot.text(min_size+1,max_size-1, 'growth', fontsize = 20, color='orange')
    subplot.set_xlabel("Abstraction size before transition")
    subplot.set_ylabel("Abstraction size after transition")
    subplot.set_aspect('equal', 'box')
    subplot.legend(bbox_to_anchor=(1.05, 1))
