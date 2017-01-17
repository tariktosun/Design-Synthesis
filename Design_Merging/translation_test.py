# path
import os, sys
file_dir = os.path.dirname(__file__) # dir of this file
src_dir = os.path.join(file_dir, './src')
sys.path.append(src_dir)
# Translate:
import Translator
# # Embedding
from Embedding import Embedding
import Embedding.Node as Node
import Embedding.Design as Design
# # PyKDL:
# import roslib
# roslib.load_manifest('orocos_kdl')
# from PyKDL import *
# Other:
import copy
import matplotlib.pyplot as plt
import networkx as nx

rootname = 'SMORES_0'
#root_dof_name = 'RightWheel' 
fileName = 'test/myThing.xml'
T = Translator.Translator()
G = T.buildNxGraph(fileName)
#newModule = T.makeModule(G, rootname, None, root_dof_name)
#moduleList = []
#T.buildModuleGraph(moduleList, fileName, rootname, root_dof_name)
pos = nx.spectral_layout(G)
nodes=nx.draw_networkx_nodes(G, pos)
edges=nx.draw_networkx_edges(G, pos)
labels=nx.draw_networkx_labels(G, pos)
edgelabels=nx.draw_networkx_edge_labels(G, pos)
plt.ion()
plt.show()

#####
D1 = T.translateDesign(fileName, rootname, 'FrontWheel')
#D2 = T.translateDesign(fileName, rootname, 'FrontWheel') # yes
D2 = T.translateDesign(fileName, 'SMORES_2', 'BackPlate') # yes
#D2 = T.translateDesign(fileName, 'SMORES_1', 'LeftWheel') # no 
#params:
types_subsumed = {1: [1,2], 2: [2]}
length_scaling = 1
params = {'types_subsumed': types_subsumed,
               'length_scaling': length_scaling}
# Embedding:
E = Embedding.Embedding(D1, D2, params)
#print E.check_kinematic_embedding_dynamic()
print E.check_topological_embedding_dynamic()