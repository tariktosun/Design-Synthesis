'''
Created on Jan 17, 2014

@author: tarik
'''
import unittest
from Embedding import Embedding
import Embedding.Node as Node
import Embedding.Design as Design
# PyKDL:
import roslib
roslib.load_manifest('kdl')
from PyKDL import * 
from math import pi, radians, degrees

class Test_Kinematics(unittest.TestCase):


    def setUp(self):
        '''
        Sets up fixtures.
        '''
        # Type subsumption:
        types_subsumed = {1: [1,2], 2: [2]}
        length_scaling = 1
        self.params = {'types_subsumed': types_subsumed,
                       'length_scaling': length_scaling}
        # Generate nodes and joints:
        b = [ Node.Node(str(i), Joint(Joint.RotZ)) for i in xrange(2) ]
        for i in xrange(len(b)):
            b[i].type = 2
        a = [ Node.Node(str(i), Joint(Joint.RotZ)) for i in xrange(3) ]
        for i in xrange(len(a)):
            a[i].type = 2
        a[1].Joint = Joint( Joint.RotY )
        
        # build structure, with Frames:
        b[0].add_child(b[1], Frame( Rotation.Identity(), Vector(2.0, 0, 0) ))
        #
        a[0].add_child(a[1], Frame( Rotation.Identity(), Vector(1.0, 0, 0) ))
        a[1].add_child(a[2], Frame( Rotation.Identity(), Vector(1.0, 0, 0) ))
        
        # Store:
        self.B = Design.Design(b[0], b)
        self.A = Design.Design(a[0], a)
        # nodemaps:
        self.AB_nodemap = {b[0]: a[0],
                           b[1]: a[2],
                           }
        
        return

    def tearDown(self):
        pass


    def test_kinematic_edge2path(self):
        '''
        Tests the edge2path condition, with kinematics.
        '''
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params, self.AB_nodemap)
        
        pass_set = [ AB_embedding ]
        
        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            
        # Set angle incorrectly:
        self.A.nodes[1].current_angle = radians(10)
        fail_set = [ AB_embedding ]    
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_edge2path(), 'Fail set ' + str(i)
        
    def test_kinematic_brute(self):
        '''
        Tests brute-force function for embedding detection:
        '''
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params)
        
        pass_set = [ AB_embedding ]
        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_embedding_brute(), 'Pass set ' + str(i)
                    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()