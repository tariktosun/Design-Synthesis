'''
Created on Jan 31, 2014

@author: tarik
'''
import unittest
import Embedding.Node as Node
import Embedding.Design as Design
from Embedding import Embedding
import Embedding.SmoresModule as SmoresModule
import Embedding.SmoresDesign as SmoresDesign
from fixtures_grasper_walker import setUpGrasperWalker

class Test_Smores_Kinematics(unittest.TestCase):


    def setUp(self):
        '''
        sets up fixtures.
        '''
        # Type subsumption:
        types_subsumed = {1: [1,2], 2: [2]}
        length_scaling = 1
        self.params = {'types_subsumed': types_subsumed,
                       'length_scaling': length_scaling}
        # Manual SMORES subdesign:
        b = [Node.Node(str(i)) for i in range(8)]
        
        #build structure:
        b[7].add_child(b[4])
        b[4].add_child(b[5])
        b[4].add_child(b[6])
        b[4].add_child(b[3])
        b[3].add_child(b[2])
        b[3].add_child(b[1])
        b[3].add_child(b[0])
        #Assign types and activity:
        for i in [4,3]:
            b[i].type = 2
        for i in [5,7,6,0,1,2]:
            b[i].type = 1
        for i in [5,6,1,2]:
            b[i].active = False
        #store:
        self.B = Design.Design(b[7], b)
        # set lengths:
        for e in self.B.edges:
            e.length = 1
        self.B.nodes[3].parent_edge.length = 2
        
        # Manual SMORES superdesign:
        a = [Node.Node(str(i)) for i in range(8)]
        
        # build structure:
        a[7].add_child(a[5])
        for i in [4,6]:
            a[5].add_child(a[i])
        a[4].add_child(a[3])
        for i in [0,1,2]:
            a[3].add_child(a[i])
        # Assign types and activity:
        for i in [3,5]:
            a[i].type = 2
        for i in [0,1,2,4,6,7]:
            a[i].type = 1
        # All nodes active by default.
        #store:
        self.A = Design.Design(a[7], a)
        # set lengths:
        for e in self.A.edges:
            e.length = 1
        #a[3].parent_edge.length = 0 incorrect.
        
        ''' The same designs, but made using the SmoresModule class: '''
        # Subdesign:
        b_smores = [ SmoresModule.SmoresModule('0',1, [2,3]), SmoresModule.SmoresModule('1',0, [2,3]) ]
        # build structure:
        b_smores[1].add_child_module( 1, b_smores[0] )
        # make a SmoresDesign and store :
        self.BSmores = SmoresDesign.SmoresDesign( b_smores[1], b_smores )
        
        # Superdesign:
        a_smores = [ SmoresModule.SmoresModule( '0', 1 ), SmoresModule.SmoresModule( '1', 2 ) ]
        # build structure:
        a_smores[1].add_child_module( 3 , a_smores[0] )
        # make a SmoresDesign and store it:
        self.ASmores = SmoresDesign.SmoresDesign( a_smores[1], a_smores )

        ''' Grasper and walker: '''
        setUpGrasperWalker(self)


    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()