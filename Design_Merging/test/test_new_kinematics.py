'''
Created on Jan 25, 2014

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
from math import pi, radians, degrees, acos
import copy

class Test_new_kinematics(unittest.TestCase):


    def setUp(self):
        '''
        Sets up fixtures.
        '''
        # Type subsumption:
        types_subsumed = {1: [1,2], 2: [2]}
        length_scaling = 1
        self.params = {'types_subsumed': types_subsumed,
                       'length_scaling': length_scaling}
        # Generate nodes and frames:
        b = [ Node.Node('b'+str(i)) for i in xrange(3) ]
        for i in xrange(len(b)):
            b[i].type = 2
        #
        a = [ Node.Node('a'+str(i)) for i in xrange(4) ]
        #         a = [Node.Node('0',Frame()),
        #              Node.Node('1',Frame(1,0,0)),
        #              Node.Node('2',Frame(1,0,0))]
        for i in xrange(len(a)):
            a[i].type = 2
        # build structure, with Joints:
        b[0].add_child(b[1], Frame(), Joint(Joint.RotZ))
        b[1].add_child(b[2], Frame(Vector(2,0,0)), Joint(Joint.RotZ))
        #
        a[0].add_child(a[1], Frame(), Joint(Joint.RotZ))
        a[1].add_child(a[2], Frame(Vector(1,0,0)), Joint(Joint.RotZ))
        a[2].add_child(a[3], Frame(Vector(1,0,0)), Joint(Joint.RotZ))
        # Store:
        self.B = Design.Design(b[0], b)
        self.A = Design.Design(a[0], a)
        # nodemaps:
        self.AB_nodemap = {b[0]: a[0],
                           b[1]: a[1],
                           b[2]: a[3],
                           }    #yes


    def tearDown(self):
        pass


    def test_kinematic_edge2path(self):
        '''
        Tests the edge2path condition, with kinematics.
        '''
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params, self.AB_nodemap)
        #         CB_embedding = Embedding.Embedding(self.C, self.B, self.params, self.CB_nodemap)
        #         CA_embedding = Embedding.Embedding(self.C, self.A, self.params, self.CA_nodemap)
        #         DB_embedding = Embedding.Embedding(self.D, self.B, self.params, self.DB_nodemap)
        #         AC_embedding = Embedding.Embedding(self.A, self.C, self.params, self.AC_nodemap)
        #         BD_embedding = Embedding.Embedding(self.B, self.D, self.params, self.BD_nodemap)
        #         EB_embedding = Embedding.Embedding(self.E, self.B, self.params, self.EB_nodemap)
        #         GF_embedding = Embedding.Embedding(self.G, self.F, self.params, self.GF_nodemap)
        #         GB_embedding = Embedding.Embedding(self.G, self.B, self.params, self.GB_nodemap)
        
        #         # Set E angles appropriately:
        #         self.E.nodes[0].current_angle = acos(1./3)
        #         self.E.nodes[1].current_angle = -2*acos(1./3)
        #         #self.E.nodes[2].current_angle = acos(1./3)
        #         self.E.nodes[2].current_angle = radians(10)
        #           
        #         # set G angles appropriately:
        #         self.G.nodes[0].current_angle = acos(1./3)
        #         self.G.nodes[1].current_angle = -2*acos(1./3)
        #         self.G.nodes[2].current_angle = acos(1./3)# + acos(1./3)
        #         self.G.nodes[3].current_angle = -2*acos(1./3)
        #         self.G.nodes[4].current_angle = 0
        
        #pass_set = [ AB_embedding, EB_embedding, GF_embedding ]
        #pass_set = [ EB_embedding, GB_embedding, GF_embedding ]
        pass_set = [ AB_embedding ]
        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            
        #fail_set = [ CB_embedding, CA_embedding, DB_embedding, AC_embedding, BD_embedding ]
        fail_set = []    
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_edge2path(), 'Fail set ' + str(i)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()