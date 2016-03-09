# path
import sys
sys.path.append('src')
sys.path.append('test')
# Translate:
import Translator
# Embedding
from Embedding import Embedding
import Embedding.Node as Node
import Embedding.Design as Design
# PyKDL:
import roslib
roslib.load_manifest('orocos_kdl')
from PyKDL import *
# Other:
import copy
import matplotlib.pyplot as plt
import networkx as nx

rootname = 'SMORES_2'
root_dof_name = 'BackPlate' 
fileName = 'test/myThing.xml'
T = Translator.Translator()
#G = T.buildNxGraph(fileName)
#newModule = T.makeModule(G, rootname, None, root_dof_name)
#moduleList = []
#T.buildModuleGraph(moduleList, fileName, rootname, root_dof_name)
D = T.translateDesign(fileName, rootname, root_dof_name)