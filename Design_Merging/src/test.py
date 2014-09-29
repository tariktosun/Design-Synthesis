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
import time
import numpy as np
from matplotlib.pyplot import *
from math import sqrt
import pdb



# Create parameters:
types_subsumed = {1: [1], 2: [2]}
length_scaling = 1
params = {'types_subsumed': types_subsumed,
                   'length_scaling': length_scaling}
subN = 5
superN = 20

subD = SmoresRandomDesign(2,subN, sqrt(subN)/2, is_subdesign=True)
superD = SmoresRandomDesign(2, superN, sqrt(superN)/2)
embedding = Embedding.Embedding(superD, subD, params)
start = time.clock()
succeeds = embedding.check_kinematic_embedding_dynamic(record_timings=True)
t = time.clock() - start
embedding.write_timings_to_file('foo.txt')

