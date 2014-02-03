'''
Script for random tree timing analysis.
Created on Feb 1, 2014

@author: tarik
'''
import sys
sys.path.append('..')
import Embedding.Node as Node
import Embedding.Design as Design
from Embedding import Embedding
from smoresRandomDesign import SmoresRandomDesign
import timeit
import time
import numpy as np
from matplotlib.pyplot import * 



# Create parameters:
types_subsumed = {1: [1], 2: [2]}
length_scaling = 1
params = {'types_subsumed': types_subsumed,
                   'length_scaling': length_scaling}

repeats = 10
trials = 1000
times = [0]*trials
subtrees = [0]*trials
supertrees = [0]*trials
boolean_results = [0]*trials


# generate testing set:
sub_nummodules = [6, 18, 30, 42, 54]
super_nummodules = [10, 50, 100, 150, 200]
num_repeats = 10

super_designs = dict( zip(super_nummodules, [[] for _ in xrange(len(super_nummodules))]))
super_counts = dict( zip(super_nummodules, [0 for _ in xrange(len(super_nummodules))]))

finished = False
while not finished:
    A = SmoresRandomDesign(2, 8)
    if len(A.modules) in super_nummodules:
        super_designs[len(A.modules)].append(A)
        super_counts[len(A.modules)] += 1
    if all([c>num_repeats for c in super_counts.values()]):
        finished = True








true_count = 0
for i in xrange(trials):
    A = RandomTree(4,7)
    B = RandomTree(4,4)
    AB_embedding = Embedding.Embedding(A, B, params)
    #times[i] = min(timeit.Timer(AB_embedding.check_topological_embedding_dynamic).repeat(repeats,1))
    #times[i] = timeit.Timer(AB_embedding.check_topological_embedding_dynamic).timeit(1)
    start = time.clock()
    AB_embedding.check_topological_embedding_dynamic()
    end = time.clock()
    times[i] = end - start
    boolean_result = AB_embedding.check_topological_embedding_dynamic()
    if boolean_result:
        assert AB_embedding.check_vertex2vertex()
        assert AB_embedding.check_edge2path()
        assert AB_embedding.check_vertex_disjointness()

    boolean_results[i] = boolean_result
    subtrees[i] = B
    supertrees[i] = A
    sys.stdout.write('%d / %d  \r' % (i, trials))
    sys.stdout.flush()
    
subnodes = [len(tree.nodes) for tree in subtrees]
supernodes = [len(tree.nodes) for tree in supertrees]
total_nodes = [subnodes[i] + supernodes[i] for i in xrange(len(subnodes))]
sub_avg_bfs = [tree.average_branching_factor for tree in subtrees]
super_avg_bfs = [tree.average_branching_factor for tree in supertrees]

print str(trials) + ' trials, ' + str(repeats) + ' repeats, ' + str(sum(times)) + ' seconds.'
figure()
plot(subnodes, times, '.')
plot(supernodes, times, '.r')
plot(total_nodes, times, '.g')
title('Nodes vs. time')
