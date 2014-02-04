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
from math import sqrt



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
#sub_nummodules = [6, 18, 30, 42, 54]
#super_nummodules = [10, 50, 100, 150, 200]
sub_nummodules = [3, 6, 9]
super_nummodules = [10,15,20]
num_repeats = 5

super_designs = {}
for n in super_nummodules:
    designs = [ SmoresRandomDesign(2, n, sqrt(n)/2) for _ in xrange(num_repeats) ]
    super_designs[n] = designs

sub_designs = {}
for n in sub_nummodules:
    designs = [ SmoresRandomDesign(2, n, sqrt(n)/2, is_subdesign=True) for _ in xrange(num_repeats) ]
    sub_designs[n] = designs

print "Beginning trials."
times = {}    
for i,N in enumerate(super_nummodules):
    if not times.has_key(N):
        times[N] = {}
    for j,M in enumerate(sub_nummodules):
        if not times[N].has_key(M):
                times[N][M] = 0
        # all spd will have N nodes, all sbd will have M nodes.  We want the average
        # time to embed a subd of M nodes in a superd of N nodes
        t = 0
        trials = 0
        for spd in super_designs[N]:
            for sbd in sub_designs[M]:
                trials +=1
                sys.stdout.write('N = %d/%d, M = %d/%d, trial =  %d/%d  \r' % (i+1,len(super_nummodules), j+1,len(sub_nummodules), trials,num_repeats*num_repeats))
                sys.stdout.flush()
                sbd.strip_inactive_nodes()
                embedding = Embedding.Embedding(spd, sbd, params)
                start = time.clock()
                succeeds = embedding.check_kinematic_embedding_dynamic()
                t += time.clock() - start
                if succeeds:
                    assert embedding.check_vertex2vertex()
                    assert embedding.check_edge2path()
                    assert embedding.check_vertex_disjointness()
        times[N][M] = t / float(num_repeats*num_repeats) 



# finished = False
# while not finished:
#     A = SmoresRandomDesign(2, 8)
#     if len(A.modules) in super_nummodules:
#         super_designs[len(A.modules)].append(A)
#         super_counts[len(A.modules)] += 1
#         print 'found! '+str(len(A.modules))
#     if all([c>num_repeats for c in super_counts.values()]):
#         finished = True




# true_count = 0
# for i in xrange(trials):
#     A = RandomTree(4,7)
#     B = RandomTree(4,4)
#     AB_embedding = Embedding.Embedding(A, B, params)
#     #times[i] = min(timeit.Timer(AB_embedding.check_topological_embedding_dynamic).repeat(repeats,1))
#     #times[i] = timeit.Timer(AB_embedding.check_topological_embedding_dynamic).timeit(1)
#     start = time.clock()
#     AB_embedding.check_topological_embedding_dynamic()
#     end = time.clock()
#     times[i] = end - start
#     boolean_result = AB_embedding.check_topological_embedding_dynamic()
#     if boolean_result:
#         assert AB_embedding.check_vertex2vertex()
#         assert AB_embedding.check_edge2path()
#         assert AB_embedding.check_vertex_disjointness()
# 
#     boolean_results[i] = boolean_result
#     subtrees[i] = B
#     supertrees[i] = A
#     sys.stdout.write('%d / %d  \r' % (i, trials))
#     sys.stdout.flush()
#     
# subnodes = [len(tree.nodes) for tree in subtrees]
# supernodes = [len(tree.nodes) for tree in supertrees]
# total_nodes = [subnodes[i] + supernodes[i] for i in xrange(len(subnodes))]
# sub_avg_bfs = [tree.average_branching_factor for tree in subtrees]
# super_avg_bfs = [tree.average_branching_factor for tree in supertrees]
# 
# print str(trials) + ' trials, ' + str(repeats) + ' repeats, ' + str(sum(times)) + ' seconds.'
# figure()
# plot(subnodes, times, '.')
# plot(supernodes, times, '.r')
# plot(total_nodes, times, '.g')
# title('Nodes vs. time')
