'''
Created on Dec 29, 2013

@author: tariktosun
'''
import os, sys
file_dir = os.path.dirname(__file__) # dir of this file
src_dir = os.path.join(file_dir, '../src')
sys.path.append(src_dir)
#
import unittest
#import Embedding.Node as Node
#import Embedding.Edge as Edge
#import Embedding.Design as Design
from Embedding import Embedding
from fixtures_topology_embedding import setUpTopologyFixtures

class Test_Toplogy_Embedding(unittest.TestCase):
     
    def setUp(self):
        ''' define fixtures for tests. '''
        setUpTopologyFixtures(self)
        
    def tearDown(self):
        pass
    
    def test_topological_embedding_dynamic(self):
        ''' NOTE: This test contains some functionality manipulations!!!'''
        
        ''' Swap functionality around to perform tests:'''
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params)
        
        self.B.nodes[2].type = 1
        for i, embedding in enumerate([ AB_embedding, CB_embedding ]):
            assert not embedding.check_topological_embedding_dynamic(), 'Functionality fail set ' + str(i)
        self.A.nodes[4].type = 1
        self.C.nodes[2].type = 1
        for i, embedding in enumerate([ AB_embedding, CB_embedding ]):
            assert embedding.check_topological_embedding_dynamic(), 'Functionality pass set ' + str(i)
        self.B.nodes[2].type = 2
        for i, embedding in enumerate([ AB_embedding, CB_embedding ]):
            assert embedding.check_topological_embedding_dynamic(), 'Functionality pass set ' + str(i)        
              
        ''' Change functionality back, and continue tests as usual. '''
        self.A.nodes[4].type = 2
        self.C.nodes[2].type = 2
        self.B.nodes[2].type = 2
        
        # pass set:
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params)
        pass_set = [AB_embedding, CB_embedding ]
        #pass_set = [ CB_embedding ]
        #pass_set = [AB_embedding]

        # fail set:
        BA_embedding = Embedding.Embedding(self.B, self.A, self.params)
        BC_embedding = Embedding.Embedding(self.B, self.C, self.params)
        fail_set = [ BA_embedding, BC_embedding ]

        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_topological_embedding_dynamic(), 'Pass set ' + str(i)
            assert embedding.check_vertex2vertex(), 'Pass set ' + str(i)
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            assert embedding.check_vertex_disjointness(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_topological_embedding_dynamic(), 'Fail set ' + str(i)
    
    def test_topological_embedding_brute(self):
        ''' NOTE: This test contains some functionality manipulations!!!'''
        
        ''' Swap functionality around to perform tests:'''
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params)
        
        self.B.nodes[2].type = 1
        for i, embedding in enumerate([ AB_embedding, CB_embedding ]):
            assert not embedding.check_topological_embedding_brute(), 'Functionality fail set ' + str(i)
        self.A.nodes[4].type = 1
        self.C.nodes[2].type = 1
        for i, embedding in enumerate([ AB_embedding, CB_embedding ]):
            assert embedding.check_topological_embedding_brute(), 'Functionality pass set ' + str(i)
        self.B.nodes[2].type = 2
        for i, embedding in enumerate([ AB_embedding, CB_embedding ]):
            assert embedding.check_topological_embedding_brute(), 'Functionality pass set ' + str(i)        
              
        ''' Change functionality back, and continue tests as usual. '''
        self.A.nodes[4].type = 2
        self.C.nodes[2].type = 2
        self.B.nodes[2].type = 2
        
        # pass set:
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params)
        pass_set = [AB_embedding, CB_embedding] # There is actually a valid CB embedding.

        # fail set:
        BA_embedding = Embedding.Embedding(self.B, self.A, self.params)
        BC_embedding = Embedding.Embedding(self.B, self.C, self.params)
        fail_set = [ BA_embedding, BC_embedding]

        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_topological_embedding_brute(), 'Pass set ' + str(i)
            assert embedding.check_vertex2vertex(), 'Pass set ' + str(i)
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            assert embedding.check_vertex_disjointness(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_topological_embedding_brute(), 'Fail set ' + str(i)
        

    def test_vertex2vertex(self):
        ''' NOTE: This test contains some functionality manipulations!!!'''
        
        ''' Swap functionality around to perform tests:'''
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params, self.AB_nodemap)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params, self.CB_nodemap)
        
        self.B.nodes[2].type = 1
        for i, embedding in enumerate([ AB_embedding, CB_embedding ]):
            assert not embedding.check_vertex2vertex(), 'Functionality fail set ' + str(i)
        self.A.nodes[4].type = 1
        self.C.nodes[3].type = 1
        for i, embedding in enumerate([ AB_embedding, CB_embedding ]):
            assert embedding.check_vertex2vertex(), 'Functionality pass set ' + str(i)
        self.B.nodes[2].type = 2
        for i, embedding in enumerate([ AB_embedding, CB_embedding ]):
            assert embedding.check_vertex2vertex(), 'Functionality pass set ' + str(i)        
              
        ''' Change functionality back, and continue tests as usual. '''
        self.A.nodes[4].type = 2
        self.C.nodes[3].type = 2
        self.B.nodes[2].type = 2
        
        # pass set:
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params, self.AB_nodemap)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params, self.CB_nodemap)
        AB_fails_ee = Embedding.Embedding(self.A, self.B, self.params, self.AB_fails_ee)
        pass_set = [ AB_embedding, CB_embedding ]

        # fail set:
        BA_embedding = Embedding.Embedding(self.B, self.A, self.params, self.AB_reversemap)
        BC_embedding = Embedding.Embedding(self.B, self.C, self.params, self.CB_reversemap)
        fail_set = [ BA_embedding, BC_embedding, AB_fails_ee ]
        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_vertex2vertex(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_vertex2vertex(), 'Fail set' + str(i)
        
    def test_edge2path(self):
        # pass set:
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params, self.AB_nodemap)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params, self.CB_nodemap)
        AB_fails_ee = Embedding.Embedding(self.A, self.B, self.params, self.AB_fails_ee)
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
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params, self.AB_nodemap)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params, self.CB_nodemap)
        CB_problematic = Embedding.Embedding(self.C, self.B, self.params, self.CB_problematic_map)
        AB_fails_ee = Embedding.Embedding(self.A, self.B, self.params, self.AB_fails_ee)
        
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