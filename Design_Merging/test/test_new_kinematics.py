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
        b2 = [ Node.Node('b2'+str(i)) for i in xrange(3) ]
        for i in xrange(len(b2)):
            b2[i].type = 2
        #
        a = [ Node.Node('a'+str(i)) for i in xrange(4) ]
        for i in xrange(len(a)):
            a[i].type = 2
        #
        a2 = [ Node.Node('a2'+str(i)) for i in xrange(4) ]
        for i in xrange(len(a2)):
            a2[i].type = 2
        #
        c = [Node.Node('c'+str(i)) for i in xrange(4)]
        for i in xrange(len(c)):
            c[i].type = 2
        #
        d = [ Node.Node(str(i)) for i in xrange(3)]
        for i in xrange(len(d)):
            d[i].type = 2
        #
        e = [Node.Node('e'+str(i)) for i in xrange(4)]
        for i in xrange(len(e)):
            e[i].type = 2
        #
        f = [Node.Node('f'+str(i)) for i in xrange(4)]
        for i in xrange(len(f)):
            f[i].type = 2
        #
        g = [Node.Node('g'+str(i)) for i in xrange(6)]
        for i in xrange(len(g)):
            g[i].type = 2
            
        # build structure, with Joints:
        b[0].add_child(b[1], Frame(), Joint(Joint.RotZ))
        b[1].add_child(b[2], Frame(Vector(2,0,0)), Joint(Joint.RotZ))
        # build structure, with Joints:
        b2[0].add_child(b2[1], Frame(Vector(1,0,0)), Joint(Joint.RotZ))
        b2[1].add_child(b2[2], Frame(Vector(1,0,0)), Joint(Joint.RotZ))
        #
        a[0].add_child(a[1], Frame(), Joint(Joint.RotZ))
        a[1].add_child(a[2], Frame(Vector(1,0,0)), Joint(Joint.RotZ))
        a[2].add_child(a[3], Frame(Vector(1,0,0)), Joint(Joint.RotZ))
        #
        a2[0].add_child(a2[1], Frame(Vector(1,0,0)), Joint(Joint.RotZ))
        a2[1].add_child(a2[2], Frame(Vector(1,0,0)), Joint(Joint.RotZ))
        a2[2].add_child(a2[3], Frame(Vector(1,0,0)), Joint(Joint.RotZ))
        #
        c[0].add_child(c[1], Frame(), Joint(Joint.RotZ))
        c[1].add_child(c[2], Frame(Vector(1,0,0)), Joint(Joint.RotY))
        c[2].add_child(c[3], Frame(Vector(1,0,0)), Joint(Joint.RotX))
        #
        d[0].add_child(d[1], Frame(), Joint(Joint.RotZ))
        d[1].add_child(d[2], Frame(Vector(1,0,0)), Joint(Joint.RotZ))
        #
        e[0].add_child(e[1], Frame(), Joint(Joint.RotZ))
        e[1].add_child(e[2], Frame(Vector(3,0,0)), Joint(Joint.RotZ))
        e[2].add_child(e[3], Frame(Vector(3,0,0)), Joint(Joint.RotZ))
        #
        f[0].add_child(f[1], Frame(), Joint(Joint.RotZ))
        f[1].add_child(f[2], Frame(Vector(2,0,0)), Joint(Joint.RotZ))
        f[2].add_child(f[3], Frame(Vector(2,0,0)), Joint(Joint.RotZ))
        #
        g[0].add_child(g[1], Frame(), Joint(Joint.RotZ))
        g[1].add_child(g[2], Frame(Vector(3,0,0)), Joint(Joint.RotZ))
        g[2].add_child(g[3], Frame(Vector(3,0,0)), Joint(Joint.RotZ))
        g[3].add_child(g[4], Frame(Vector(3,0,0)), Joint(Joint.RotZ))
        g[4].add_child(g[5], Frame(Vector(3,0,0)), Joint(Joint.RotZ))  
        
        # Store:
        self.B = Design.Design(b[0], b)
        self.A = Design.Design(a[0], a)
        self.C = Design.Design(c[0], c)
        self.B2 = Design.Design(b2[0], b2)
        self.A2 = Design.Design(a2[0], a2)
        self.D = Design.Design(d[0], d)
        self.E = Design.Design(e[0], e)
        self.F = Design.Design(f[0], f)
        self.G = Design.Design(g[0], g)
        
        # nodemaps:
        self.AB_nodemap = {b[0]: a[0],
                           b[1]: a[1],
                           b[2]: a[3],
                           }    #yes
        self.AB_nodemap2 = {b[0]: a[0],
                           b[1]: a[2],
                           b[2]: a[3],
                           }    #no
        self.A2B2_nodemap = {b2[0]: a2[0],
                           b2[1]: a2[1],
                           b2[2]: a2[3],
                           }    #no;
        self.A2B2_nodemap2 = {b2[0]: a2[1],
                           b2[1]: a2[2],
                           b2[2]: a2[3],
                           }    #yes; tests root in non-root emedding.
        self.CB_nodemap = {b[0]: c[0],
                           b[1]: c[1], 
                           b[2]: c[3],
                           }    # no; kinematic mismatch.
        self.CA_nodemap = {a[0]: c[0],
                           a[1]: c[1],
                           a[2]: c[2],
                           a[3]: c[3],
                           } #no; kinematic mismatch
        self.DB_nodemap = {b[0]: d[0],
                           b[1]: d[1],
                           b[2]: d[2],} # too short
        self.AC_nodemap = dict(zip(self.CA_nodemap.values(), self.CA_nodemap.keys())) #no
        self.BD_nodemap = dict(zip(self.DB_nodemap.values(), self.DB_nodemap.keys())) #no
        self.EB_nodemap = {b[0]: e[0],
                           b[1]: e[1],
                           b[2]: e[3],
                           } #yes
        self.GF_nodemap = {f[0]: g[0],
                           f[1]: g[1],
                           f[2]: g[3],
                           f[3]: g[5],
                           } #yes
        self.GB2_nodemap = {b2[0]: g[0],
                            b2[1]: g[3],
                            b2[2]: g[5],
                           } #yes
    def tearDown(self):
        pass


    def test_kinematic_edge2path(self):
        '''
        Tests the edge2path condition, with kinematics.
        '''
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params, self.AB_nodemap)
        AB_embedding2 = Embedding.Embedding(self.A, self.B, self.params, self.AB_nodemap2)
        A2B2_embedding = Embedding.Embedding(self.A2, self.B2, self.params, self.A2B2_nodemap)
        A2B2_embedding2 = Embedding.Embedding(self.A2, self.B2, self.params, self.A2B2_nodemap2)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params, self.CB_nodemap)
        CA_embedding = Embedding.Embedding(self.C, self.A, self.params, self.CA_nodemap)
        DB_embedding = Embedding.Embedding(self.D, self.B, self.params, self.DB_nodemap)
        AC_embedding = Embedding.Embedding(self.A, self.C, self.params, self.AC_nodemap)
        BD_embedding = Embedding.Embedding(self.B, self.D, self.params, self.BD_nodemap)
        EB_embedding = Embedding.Embedding(self.E, self.B, self.params, self.EB_nodemap)
        GF_embedding = Embedding.Embedding(self.G, self.F, self.params, self.GF_nodemap)
        GB2_embedding = Embedding.Embedding(self.G, self.B2, self.params, self.GB2_nodemap)
        
        # Set E angles appropriately:
        self.E.nodes[1].parent_edge.current_angle = acos(1./3)
        self.E.nodes[2].parent_edge.current_angle = -2*acos(1./3)
        #self.E.nodes[2].current_angle = acos(1./3)
        self.E.nodes[3].parent_edge.current_angle = radians(10)
        #           
        # set G angles appropriately:
        self.G.nodes[1].parent_edge.current_angle = acos(1./3)
        self.G.nodes[2].parent_edge.current_angle = -2*acos(1./3)
        self.G.nodes[3].parent_edge.current_angle = acos(1./3)# + acos(1./3)
        self.G.nodes[4].parent_edge.current_angle = -2*acos(1./3)
        self.G.nodes[5].parent_edge.current_angle = 0
        
        #pass_set = [ AB_embedding, EB_embedding, GF_embedding ]
        #pass_set = [ EB_embedding, GB_embedding, GF_embedding ]
        pass_set = [ AB_embedding, A2B2_embedding2, EB_embedding, GF_embedding, GB2_embedding  ]
        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            
        #fail_set = [ CB_embedding, CA_embedding, DB_embedding, AC_embedding, BD_embedding ]
        fail_set = [ CB_embedding, AB_embedding2, A2B2_embedding, CA_embedding, 
                    AC_embedding, DB_embedding, BD_embedding]    
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
        GF_embedding = Embedding.Embedding(self.G, self.F, self.params)
        GB2_embedding = Embedding.Embedding(self.G, self.B2, self.params)
        
        # Set angle incorrectly:
        self.A.nodes[2].parent_edge.current_angle = radians(10)
        
        # Set E angles appropriately:
        delta = radians(50) # Fails for 60.
        self.E.nodes[1].parent_edge.current_angle = acos(1./3) + delta
        self.E.nodes[2].parent_edge.current_angle = -2*acos(1./3) + delta
        self.E.nodes[3].parent_edge.current_angle = acos(1./3) + delta
        
        # set G angles appropriately:
        self.G.nodes[1].parent_edge.current_angle = acos(1./3) + delta
        self.G.nodes[2].parent_edge.current_angle = -2*acos(1./3) + delta
        self.G.nodes[3].parent_edge.current_angle = acos(1./3) + delta# + acos(1./3)
        self.G.nodes[4].parent_edge.current_angle = -2*acos(1./3) + delta
        self.G.nodes[5].parent_edge.current_angle = 0 + delta
          
        pass_set = [ AB_embedding, EB_embedding, GF_embedding, GB2_embedding ]
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