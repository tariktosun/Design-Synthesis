import sys
sys.path.append('..')
import Embedding.Node as Node
import Embedding.Design as Design
from Embedding import Embedding
from smoresRandomDesign import SmoresRandomDesign
import time
from math import sqrt

# Select experiment parameters 
subN = 20 
superN = 30 
repetitions = 20 

# Create running parameters:
types_subsumed = {1: [1], 2: [2]}
length_scaling = 1
params = {'types_subsumed': types_subsumed,
                   'length_scaling': length_scaling}

for iter in xrange(1,repetitions+1):
    # Create designs
    subD = SmoresRandomDesign(2,subN, sqrt(subN)/2, is_subdesign=True)
    superD = SmoresRandomDesign(2, superN, sqrt(superN)/2)
    embedding = Embedding.Embedding(superD, subD, params)
    
    # run experiment
    start = time.time()
    print('Beginning to check embedding with ' + str(subN) +
          ' modules in subdesign and ' + str(superN) + ' modules in superdesign.')
    succeeds = embedding.check_kinematic_embedding_dynamic(record_timings=True)
    t = time.time() - start
    print('Finished experiment ' +str(iter)+ ' in ' + str(t) + ' seconds.')
    # write to text file
    embedding.write_timings_to_file(str(subN) + '_' + str(superN) + '-'+str(repetitions)+'reps.txt')

