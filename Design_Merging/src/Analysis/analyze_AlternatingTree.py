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
from RandomTree import RandomTree
from AlternatingTree import AlternatingTree
import timeit
import time
import numpy as np
from matplotlib.pyplot import * 
from matplotlib.backends.backend_pdf import PdfPages



# Create parameters:
types_subsumed = {1: [1], 2: [2]}
length_scaling = 1
params = {'types_subsumed': types_subsumed,
                   'length_scaling': length_scaling}

# repeats = 10
# trials = 1000
# times = [0]*trials
# subtrees = [0]*trials
# supertrees = [0]*trials
# boolean_results = [0]*trials

trials = 20
K = 2
D = 6
times = {}

k=2
print 'running trials.'
#for k in xrange(1,K+1):     #branching factor
for d in xrange(1,D+1): #depth
    for trial in xrange(trials):
        sys.stdout.write('k = %d/%d, d = %d/%d, trial =  %d/%d  \r' % (k,K, d,D, trial,trials))
        sys.stdout.flush()
        t = 0
        B = AlternatingTree('random',k,d)
        A = AlternatingTree('alternating',k,d*2)
        AB_embedding = Embedding.Embedding(A, B, params)
        start = time.clock()
        AB_embedding.check_topological_embedding_dynamic()
        t += time.clock() - start
    if not times.has_key(k):
        times[k] = {}
    times[k][d] = t/float(trials)
    

T = times[2].values()
numnodes = [(2**d)-1 for d in range(1,D+1)]

# fit curve:
pfit = np.polyfit(np.array(numnodes), np.array(T), 3)
def cubicPoly(x, pfit):
    return pfit[3] + pfit[2]*x + pfit[1]*x**2 + pfit[0]*x**3
fitcurve = [cubicPoly(x, pfit) for x in range(1,70)]

#plot:
figure()
p1 = plot(numnodes,T, 'o', markersize=10, label='Data')
p2 = plot(range(1,70), fitcurve, 'r--', label='Cubic fit line')
p3 = title('Alternating Binary Tree')
p4 = xlabel('Number of nodes (N)')
p5 = ylabel('Average CPU time (seconds)')
p6 = legend()
p7 = xticks(numnodes)

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



