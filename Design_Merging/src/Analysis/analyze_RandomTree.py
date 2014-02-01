'''
Script for random tree timing analysis.
Created on Feb 1, 2014

@author: tarik
'''

import Embedding.Node as Node
import Embedding.Design as Design
from Embedding import Embedding
from RandomTree import RandomTree
import timeit
import sys
import numpy
from matplotlib.pyplot import * 

# Create parameters:
types_subsumed = {1: [1,2], 2: [2]}
length_scaling = 1
params = {'types_subsumed': types_subsumed,
                   'length_scaling': length_scaling}

repeats = 5
trials = 100
times = [0]*trials
subtrees = [0]*trials
supertrees = [0]*trials
boolean_results = [0]*trials

true_count = 0
for i in xrange(trials):
    A = RandomTree(4,7)
    B = RandomTree(4,4)
    AB_embedding = Embedding.Embedding(A, B, params)
    boolean_result = AB_embedding.check_topological_embedding_dynamic()
    times[i] = timeit.Timer(AB_embedding.check_topological_embedding_dynamic).timeit(repeats)
    boolean_results[i] = boolean_result
    subtrees[i] = B
    supertrees[i] = A
    sys.stdout.write('%d / %d  \r' % (i, trials))
    sys.stdout.flush()
    
subnodes = [len(tree.nodes) for tree in subtrees]
supernodes = [len(tree.nodes) for tree in supertrees]
print str(trials) + ' trials, ' + str(repeats) + ' repeats, ' + str(sum(times)) + ' seconds.'


