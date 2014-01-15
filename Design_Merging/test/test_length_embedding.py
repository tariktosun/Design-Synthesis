'''
Created on Jan 14, 2014

@author: tariktosun
'''
import unittest
#import Embedding.Node as Node
#import Embedding.Edge as Edge
#import Embedding.Design as Design
from Embedding import Embedding
from fixtures_topology_embedding import setUpTopologyFixtures

class Test_Length_Embedding(unittest.TestCase):

    def setUp(self):
        setUpTopologyFixtures(self)
        # These tests operate by changing the edge lengths in the designs used
        # previously.
        
        # note: CB_nodemap in the topology fixtures is actually an invalid mapping.
        b = self.B.nodes
        c = self.C.nodes
        self.CB_valid_nodemap = {b[3]:c[4],
                       b[2]:c[2],
                       b[1]:c[1],
                       b[0]:c[0],
                       }
        
    def tearDown(self):
        pass
    
    def _set_valid_lengths(self):
        '''
        Sets edge lengths in A, B, and C so that all the old embeddings will 
        still be valid.
        '''
        self.C.nodes[0].parent_edge.length = 1
        self.C.nodes[1].parent_edge.length = 1
        self.C.nodes[2].parent_edge.length = 0.5
        self.C.nodes[3].parent_edge.length = 0.5
        
        self.A.nodes[0].parent_edge.length = 0.5
        self.A.nodes[1].parent_edge.length = 0.5
        self.A.nodes[2].parent_edge.length = 0.5
        self.A.nodes[3].parent_edge.length = 0.5
        self.A.nodes[4].parent_edge.length = 1
        
        self.B.nodes[0].parent_edge.length = 1
        self.B.nodes[1].parent_edge.length = 1
        self.B.nodes[2].parent_edge.length = 1
        
        pass
    
    def _set_invalid_lengths(self):
        '''
        Sets invalid lengths in A, B, and C, so that none of the embeddings will
        be valid anymore.
        '''
        self.C.nodes[0].parent_edge.length = 1
        self.C.nodes[1].parent_edge.length = 1
        self.C.nodes[2].parent_edge.length = 2  # must be 2 so that B won't embed.
        self.C.nodes[3].parent_edge.length = 1
        
        self.A.nodes[0].parent_edge.length = 1
        self.A.nodes[1].parent_edge.length = 1
        self.A.nodes[2].parent_edge.length = 1
        self.A.nodes[3].parent_edge.length = 1
        self.A.nodes[4].parent_edge.length = 1
        
        self.B.nodes[0].parent_edge.length = 1
        self.B.nodes[1].parent_edge.length = 1
        self.B.nodes[2].parent_edge.length = 1
        
    def _set_zero_lengths(self):
        self.C.nodes[0].parent_edge.length = 0
        self.C.nodes[1].parent_edge.length = 0
        self.C.nodes[2].parent_edge.length = 0
        self.C.nodes[3].parent_edge.length = 0
        
        self.A.nodes[0].parent_edge.length = 0
        self.A.nodes[1].parent_edge.length = 0
        self.A.nodes[2].parent_edge.length = 0
        self.A.nodes[3].parent_edge.length = 0
        self.A.nodes[4].parent_edge.length = 0
        
        self.B.nodes[0].parent_edge.length = 0
        self.B.nodes[1].parent_edge.length = 0
        self.B.nodes[2].parent_edge.length = 0

    def test_edge2path(self):
        ''' pass set, zero length: '''
        self._set_zero_lengths()
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params, self.AB_nodemap)
        #CB_embedding = Embedding.Embedding(self.C, self.B, self.params, self.CB_nodemap)
        CB_valid_embedding = Embedding.Embedding(self.C, self.B, self.params, self.CB_valid_nodemap)
        #AB_fails_ee = Embedding.Embedding(self.A, self.B, self.params, self.AB_fails_ee)
        pass_set = [AB_embedding, CB_valid_embedding ]#, AB_fails_ee]

        for i, embedding in enumerate(pass_set):
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            
        ''' Now set valid nonzero lengths.  Everything should still pass. '''
        self._set_valid_lengths()
        for i, embedding in enumerate(pass_set):
            assert embedding.check_edge2path(), 'Pass set ' + str(i)

        ''' Set invalid non zero lengths.  Everything should now fail. '''
        self._set_invalid_lengths()
        fail_set = pass_set
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_edge2path(), 'Fail set ' + str(i)
    

    def test_length_embedding_dynamic(self):
        ''' 
        Tests dynamic programming implementation, with length embedding.
        '''
        
        ''' Valid zero length:'''
        self._set_zero_lengths()
        # pass set:
        AB_embedding = Embedding.Embedding(self.A, self.B, self.params)
        CB_embedding = Embedding.Embedding(self.C, self.B, self.params)
        pass_set = [AB_embedding, CB_embedding ]

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
        
        
        ''' Valid nonzero length: '''
        self._set_valid_lengths()
        for i, embedding in enumerate(pass_set):
            assert embedding.check_topological_embedding_dynamic(), 'Pass set ' + str(i)
            assert embedding.check_vertex2vertex(), 'Pass set ' + str(i)
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            assert embedding.check_vertex_disjointness(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_topological_embedding_dynamic(), 'Fail set ' + str(i)
            
        ''' invalid nonzero length: '''
        self._set_invalid_lengths()
        fail_set += pass_set
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_topological_embedding_dynamic(), 'Fail set ' + str(i)
            
            
    def test_topological_embedding_brute(self):
        # note copied from other file.
        
        ''' Valid zero length:'''
        self._set_zero_lengths()
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
            
        ''' valid nonzero length:'''
        self._set_valid_lengths()
        for i, embedding in enumerate(pass_set):
            assert embedding.check_topological_embedding_brute(), 'Pass set ' + str(i)
            assert embedding.check_vertex2vertex(), 'Pass set ' + str(i)
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            assert embedding.check_vertex_disjointness(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_topological_embedding_brute(), 'Fail set ' + str(i)
            
        ''' invalid nonzero length: '''
        self._set_invalid_lengths()
        fail_set += pass_set    # everything fails now
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_topological_embedding_brute(), 'Fail set ' + str(i)
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()