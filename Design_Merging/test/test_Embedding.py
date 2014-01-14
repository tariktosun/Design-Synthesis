'''
Created on Dec 29, 2013

@author: tariktosun
'''
import unittest
import Embedding.Node as Node
#import Embedding.Edge as Edge
import Embedding.Design as Design
from Embedding import Embedding

class Test_Embedding(unittest.TestCase):
    
    
    def setUp(self):
        ''' define fixtures for tests. '''
        b = [0]*4
        a = [0]*6
        c = [0]*5
        for i in xrange(len(b)):
            b[i] = Node.Node(str(i))
        for i in xrange(len(a)):
            a[i] = Node.Node(str(i))
        for i in xrange(len(c)):
            c[i] = Node.Node(str(i))
        # build structure:
        # subdesign:
        b[3].add_child(b[2])
        b[2].add_child(b[1])
        b[2].add_child(b[0])
        #
        b[1].is_end_effector = True
        b[0].is_end_effector = True
        # superdesign (good)
        a[5].add_child(a[4])
        a[4].add_child(a[3])
        a[4].add_child(a[2])
        a[3].add_child(a[1])
        a[2].add_child(a[0])
        #
        a[0].is_end_effector = True
        a[1].is_end_effector = True
        #superdesign (violates PVD in one case)
        c[4].add_child(c[3])
        c[3].add_child(c[2])
        c[2].add_child(c[1])
        c[2].add_child(c[0])
        #
        c[1].is_end_effector = True
        c[0].is_end_effector = True
        
        # Store as class variables:
        self.B = Design.Design(b[3])
        self.A = Design.Design(a[5])
        self.AB_nodemap = {b[0]:a[0],
                        b[1]:a[1],
                        b[2]:a[4],
                        b[3]:a[5],
                        }
        self.C = Design.Design(c[4])
        self.CB_nodemap = {b[3]:c[4],
                           b[2]:c[3],
                           b[1]:c[1],
                           b[0]:c[0],
                           }
        
        # reverse maps:
        self.AB_reversemap = dict (zip(self.AB_nodemap.values(),self.AB_nodemap.keys()))
        self.CB_reversemap = dict (zip(self.CB_nodemap.values(),self.CB_nodemap.keys()))
        
        # problematic nodemap for CB generated by (problematic) brute force:
        self.CB_problematic_map = {b[3]:c[4],
                               b[2]:c[3],
                               b[1]:c[2],
                               b[0]:c[1],
                               }
        
        # Problematic AB map which maps B's end effectors to A nodes with children.
        self.AB_fails_ee = {b[0]:a[2],
                        b[1]:a[3],
                        b[2]:a[4],
                        b[3]:a[5],
                        }
        
    def tearDown(self):
        pass
    
    def test_topological_embedding_dynamic(self):
        # pass set:
        AB_embedding = Embedding.Embedding(self.A, self.B)
        CB_embedding = Embedding.Embedding(self.C, self.B)
        pass_set = [AB_embedding, CB_embedding ]
        #pass_set = [ CB_embedding ]
        #pass_set = [AB_embedding]

        # fail set:
        BA_embedding = Embedding.Embedding(self.B, self.A)
        BC_embedding = Embedding.Embedding(self.B, self.C)
        fail_set = [ BA_embedding, BC_embedding ]

        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_topological_embedding_dynamic(), 'Pass set ' + str(i)
            assert embedding.check_vertex2vertex(), 'Pass set ' + str(i)
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            assert embedding.check_vertex_disjointness(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_topological_embedding_dynamic(), 'Fail set ' + str(i)
    
    def test_topological_embedding_brute(self):
        # pass set:
        AB_embedding = Embedding.Embedding(self.A, self.B)
        CB_embedding = Embedding.Embedding(self.C, self.B)
        pass_set = [AB_embedding, CB_embedding] # There is actually a valid CB embedding.

        # fail set:
        BA_embedding = Embedding.Embedding(self.B, self.A)
        BC_embedding = Embedding.Embedding(self.B, self.C)
        fail_set = [ BA_embedding, BC_embedding]

        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_topological_embedding_brute(), 'Pass set ' + str(i)
            assert embedding.check_vertex2vertex(), 'Pass set ' + str(i)
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            assert embedding.check_vertex_disjointness(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_topological_embedding_brute(), 'Fail set ' + str(i)
        

    def test_vertex2vertex(self):
        # pass set:
        AB_embedding = Embedding.Embedding(self.A, self.B, self.AB_nodemap)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.CB_nodemap)
        AB_fails_ee = Embedding.Embedding(self.A, self.B, self.AB_fails_ee)
        pass_set = [ AB_embedding, CB_embedding ]

        # fail set:
        BA_embedding = Embedding.Embedding(self.B, self.A, self.AB_reversemap)
        BC_embedding = Embedding.Embedding(self.B, self.C, self.CB_reversemap)
        fail_set = [ BA_embedding, BC_embedding, AB_fails_ee ]
        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_vertex2vertex(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_vertex2vertex(), 'Fail set' + str(i)
        
    def test_edge2path(self):
        # pass set:
        AB_embedding = Embedding.Embedding(self.A, self.B, self.AB_nodemap)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.CB_nodemap)
        AB_fails_ee = Embedding.Embedding(self.A, self.B, self.AB_fails_ee)
        pass_set = [AB_embedding, CB_embedding, AB_fails_ee]

        # fail set:
        #BA_embedding = Embedding.Embedding(self.B, self.A, self.AB_reversemap)
        #BC_embedding = Embedding.Embedding(self.B, self.C, self.CB_reversemap)
        #fail_set = [ BA_embedding, BC_embedding ]
        fail_set = []
        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_edge2path(), 'Fail set ' + str(i)
        #assert self.check_edge2path(self.A, self.B, self.AB_nodemap)
        
    def test_vertex_disjointness(self):
        # pass set:
        AB_embedding = Embedding.Embedding(self.A, self.B, self.AB_nodemap)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.CB_nodemap)
        CB_problematic = Embedding.Embedding(self.C, self.B, self.CB_problematic_map)
        AB_fails_ee = Embedding.Embedding(self.A, self.B, self.AB_fails_ee)
        
        pass_set = [AB_embedding, AB_fails_ee]

        # fail set:
        #BA_embedding = Embedding.Embedding(self.B, self.A, self.AB_reversemap)
        #BC_embedding = Embedding.Embedding(self.B, self.C, self.CB_reversemap)
        #fail_set = [ BA_embedding, BC_embedding ]
        
        fail_set = [CB_embedding, CB_problematic]
        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_vertex_disjointness(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_vertex_disjointness(), 'Fail set ' + str(i)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()