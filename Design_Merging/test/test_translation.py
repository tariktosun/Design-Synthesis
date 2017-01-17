'''
Created March 9, 2016

@author: tarik
'''
# path
import os, sys
file_dir = os.path.dirname(__file__) # dir of this file
src_dir = os.path.join(file_dir, '../src')
sys.path.append(src_dir)
sys.path.append(file_dir)
#unittest
import unittest
# Translate:
import Translator 
# Embedding
from Embedding import Embedding
import Embedding.Node as Node
import Embedding.Design as Design
# PyKDL:
#import roslib
#roslib.load_manifest('orocos_kdl')
#from PyKDL import *
# Other:
import copy
import networkx as nx
import matplotlib.pyplot as plt

class Test_Translation(unittest.TestCase):


    def setUp(self):
        '''
        Sets up fixtures.
        '''
        self.fileName = 'myThing.xml'

    def tearDown(self):
        pass
    
    def testParseXML(self):
        T = Translator.Translator()
        (moduleNames, xConnections) = T.parseXML(self.fileName)
        assert len(moduleNames)==3
        assert len(xConnections)==2 

    def testBuildNxGraph(self):
        T = Translator.Translator()
        G = T.buildNxGraph(self.fileName)
        assert len(G.nodes())==3
        assert len(G.edges())==2
        # pos = nx.spring_layout(G)
        # nodes=nx.draw_networkx_nodes(G, pos)
        # edges=nx.draw_networkx_edges(G, pos)
        # labels=nx.draw_networkx_labels(G, pos)
        # plt.show()

    def testBuildModuleGraph(self):
        rootname = 'SMORES_0'
        root_dof_name = 'FrontWheel'
        T = Translator.Translator()
        moduleList = []
        T.buildModuleGraph(moduleList, self.fileName, rootname, root_dof_name)
        assert len(moduleList) == 3
        names = [m.name for m in moduleList]
        assert names == ['SMORES_0', 'SMORES_1', 'SMORES_2']
        # test other rootings:
        # SMORES_2
        rootname = 'SMORES_2'
        root_dof_name = 'BackPlate'
        moduleList = []
        T.buildModuleGraph(moduleList, self.fileName, rootname, root_dof_name)
        assert len(moduleList) == 3
        # SMORES_1 is in the middle, so we have to use a side wheel as root:
        rootname = 'SMORES_1'
        root_dof_name = 'RightWheel'
        moduleList = []
        T.buildModuleGraph(moduleList, self.fileName, rootname, root_dof_name)
        assert len(moduleList) == 3

    def testTranslateDesign(self):
        rootname = 'SMORES_0'
        root_dof_name = 'FrontWheel'
        T = Translator.Translator()
        D = T.translateDesign(self.fileName, rootname, root_dof_name)
        D.check_validity()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()