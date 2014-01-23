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
from math import pi, radians, degrees, acos
import copy

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
        #
        a = [ Node.Node(str(i), Joint(Joint.RotZ)) for i in xrange(3) ]
        for i in xrange(len(a)):
            a[i].type = 2
        a[1].Joint = Joint( Joint.RotY )
        #
        c = [ Node.Node('0', Joint(Joint.RotZ)),
              Node.Node('1', Joint(Joint.RotY)),
              Node.Node('2', Joint(Joint.RotX)), ]
        for i in xrange(len(c)):
            c[i].type = 2
        #
        d = [ Node.Node(str(i), Joint(Joint.RotZ)) for i in xrange(2) ]
        for i in xrange(len(d)):
            d[i].type = 2
        #
        e = [ Node.Node(str(i), Joint(Joint.RotZ)) for i in xrange(3)]
        for i in xrange(len(e)):
            e[i].type = 2
        #
        f = [ Node.Node(str(i), Joint(Joint.RotZ)) for i in xrange(3)]
        for i in xrange(len(f)):
            f[i].type = 2
        #
        g = [ Node.Node(str(i), Joint(Joint.RotZ)) for i in xrange(5) ]
        for i in xrange(len(g)):
            g[i].type = 2
        
        # build structure, with Frames:
        b[0].add_child(b[1], Frame( Rotation.Identity(), Vector(2.0, 0, 0) ))
        #
        a[0].add_child(a[1], Frame( Rotation.Identity(), Vector(1.0, 0, 0) ))
        a[1].add_child(a[2], Frame( Rotation.Identity(), Vector(1.0, 0, 0) ))
        #
        c[0].add_child(c[1], Frame( Rotation.Identity(), Vector(1.0, 0, 0) ))
        c[1].add_child(c[2], Frame( Rotation.Identity(), Vector(1.0, 0, 0) ))
        #
        d[0].add_child(d[1], Frame( Rotation.Identity(), Vector(1.0, 0, 0) ))
        #
        e[0].add_child(e[1], Frame( Rotation.Identity(), Vector(3.0, 0, 0) ))
        e[1].add_child(e[2], Frame( Rotation.Identity(), Vector(3.0, 0, 0) ))
        #
        f[0].add_child(f[1], Frame( Rotation.Identity(), Vector(2.0, 0, 0) ))
        f[1].add_child(f[2], Frame( Rotation.Identity(), Vector(2.0, 0, 0) ))
        #
        g[0].add_child(g[1], Frame( Rotation.Identity(), Vector(3.0, 0, 0) ))
        g[1].add_child(g[2], Frame( Rotation.Identity(), Vector(3.0, 0, 0) ))
        g[2].add_child(g[3], Frame( Rotation.Identity(), Vector(3.0, 0, 0) ))
        g[3].add_child(g[4], Frame( Rotation.Identity(), Vector(3.0, 0, 0) ))
        
        # Store:
        self.B = Design.Design(b[0], b)
        self.A = Design.Design(a[0], a)
        self.C = Design.Design(c[0], c)
        self.D = Design.Design(d[0], d)
        self.E = Design.Design(e[0], e)
        self.F = Design.Design(f[0], f)
        self.G = Design.Design(g[0], g)
        
        # nodemaps:
        self.AB_nodemap = {b[0]: a[0],
                           b[1]: a[2],
                           }    #yes
        self.CB_nodemap = {b[0]: c[0],
                           b[1]: c[2],
                           }    #no
        self.CA_nodemap = {a[0]: c[0],
                           a[1]: c[1],
                           a[2]: c[2],
                           }    #no
        self.DB_nodemap = {b[0]: d[0],
                           b[1]: d[1]} #no
        self.AC_nodemap = dict(zip(self.CA_nodemap.values(), self.CA_nodemap.keys())) #no
        self.BD_nodemap = dict(zip(self.DB_nodemap.values(), self.DB_nodemap.keys())) #no
        self.EB_nodemap = {b[0]: e[0],
                           b[1]: e[2],
                           } #yes
        self.GF_nodemap = {f[0]: g[0],
                           f[1]: g[2],
                           f[2]: g[4],
                           } #yes
        self.GB_nodemap = {b[0]: g[2],
                           b[1]: g[4],
                           }
        
        return

    def tearDown(self):
        pass


    def test_kinematic_edge2path(self):
        '''
        Tests the edge2path condition, with kinematics.
        '''
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params, self.AB_nodemap)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params, self.CB_nodemap)
        CA_embedding = Embedding.Embedding(self.C, self.A, self.params, self.CA_nodemap)
        DB_embedding = Embedding.Embedding(self.D, self.B, self.params, self.DB_nodemap)
        AC_embedding = Embedding.Embedding(self.A, self.C, self.params, self.AC_nodemap)
        BD_embedding = Embedding.Embedding(self.B, self.D, self.params, self.BD_nodemap)
        EB_embedding = Embedding.Embedding(self.E, self.B, self.params, self.EB_nodemap)
        GF_embedding = Embedding.Embedding(self.G, self.F, self.params, self.GF_nodemap)
        GB_embedding = Embedding.Embedding(self.G, self.B, self.params, self.GB_nodemap)
        
        # Set E angles appropriately:
        self.E.nodes[0].current_angle = acos(1./3)
        self.E.nodes[1].current_angle = -2*acos(1./3)
        #self.E.nodes[2].current_angle = acos(1./3)
        self.E.nodes[2].current_angle = radians(10)
        
        # set G angles appropriately:
        self.G.nodes[0].current_angle = acos(1./3)
        self.G.nodes[1].current_angle = -2*acos(1./3)
        self.G.nodes[2].current_angle = acos(1./3)# + acos(1./3)
        self.G.nodes[3].current_angle = -2*acos(1./3)
        self.G.nodes[4].current_angle = 0
        
        #pass_set = [ AB_embedding, EB_embedding, GF_embedding ]
        pass_set = [ EB_embedding, GB_embedding, GF_embedding ]
        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            
        # Set angle incorrectly:
        self.A.nodes[1].current_angle = radians(10)
        fail_set = [ CB_embedding, CA_embedding, DB_embedding, AC_embedding, BD_embedding ]    
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_edge2path(), 'Fail set ' + str(i)
        
    def test_kinematic_brute(self):
        '''
        Tests brute-force function for embedding detection:
        '''
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params)
        CA_embedding = Embedding.Embedding(self.C, self.A, self.params)
        DB_embedding = Embedding.Embedding(self.D, self.B, self.params)
        AC_embedding = Embedding.Embedding(self.A, self.C, self.params)
        BD_embedding = Embedding.Embedding(self.B, self.D, self.params)
        EB_embedding = Embedding.Embedding(self.E, self.B, self.params)
        GF_embedding = Embedding.Embedding(self.G, self.F, self.params, self.GF_nodemap)
        GB_embedding = Embedding.Embedding(self.G, self.B, self.params, self.GB_nodemap)
        
        # Set angle incorrectly:
        self.A.nodes[1].current_angle = radians(10)
        
        # Set E angles appropriately:
        delta = radians(50) # Fails for 60.
        self.E.nodes[0].current_angle = acos(1./3) + delta
        self.E.nodes[1].current_angle = -2*acos(1./3) + delta
        self.E.nodes[2].current_angle = acos(1./3) + delta
        
        # set G angles appropriately:
        self.G.nodes[0].current_angle = acos(1./3) + delta
        self.G.nodes[1].current_angle = -2*acos(1./3) + delta
        self.G.nodes[2].current_angle = acos(1./3) + delta# + acos(1./3)
        self.G.nodes[3].current_angle = -2*acos(1./3) + delta
        self.G.nodes[4].current_angle = 0 + delta
          
        pass_set = [ AB_embedding, EB_embedding, GF_embedding, GB_embedding ]
        #pass_set = [ AB_embedding ]
          
        for i, embedding in enumerate(pass_set):
            assert embedding.check_kinematic_embedding_brute(), 'Pass set ' + str(i)
            assert embedding.check_vertex2vertex(), 'Pass set ' + str(i)
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            assert embedding.check_vertex_disjointness(), 'Pass set ' + str(i)
          
        fail_set = [ CB_embedding , CA_embedding, DB_embedding, AC_embedding, BD_embedding ]
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_kinematic_embedding_brute(), 'Fail set ' + str(i)
                    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()