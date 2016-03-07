'''
Created on Feb 1, 2014

@author: tarik
'''
import unittest
import Embedding.Node as Node
import Embedding.Design as Design
from Embedding import Embedding
from Analysis.RandomTree import RandomTree
from Analysis.AlternatingTree import AlternatingTree

class TestAnalysis(unittest.TestCase):


    def setUp(self):
        ''' set up fixtures for tests. '''
        types_subsumed = {1: [1], 2: [2]}
        length_scaling = 1
        self.params = {'types_subsumed': types_subsumed,
                   'length_scaling': length_scaling}


    def tearDown(self):
        pass


    def test_RandomTree(self):
        ''' Tests that the GrowRandomTree function is behaving properly. '''
        r = RandomTree(4, 1)
        assert len(r.nodes) == 1
        for _ in xrange(100):
            r = RandomTree(4,2)
            assert len(r.root_node.children)<=4
            assert len(r.nodes) <= 5
            
    def test_RandomTree_embedding(self):
        ''' Basic test of embedding for randomTrees. '''
        B = RandomTree(4,1)
        A = RandomTree(4,2)
        AB_embedding = Embedding.Embedding(A, B, self.params)
        assert AB_embedding.check_topological_embedding_dynamic()
        assert AB_embedding.check_vertex2vertex()
        assert AB_embedding.check_edge2path()
        assert AB_embedding.check_vertex_disjointness()
        
    def test_AlternatingTree(self):
        ''' Tests that alternating tree is behaving properly. '''
        for i in xrange(20):
            #print i
            for n in xrange(1,6):
                B = AlternatingTree('random', 2, n)
                A = AlternatingTree('alternating', 2, 2*n)
                AB_embedding = Embedding.Embedding(A, B, self.params)
                assert AB_embedding.check_topological_embedding_dynamic()
                assert AB_embedding.check_vertex2vertex()
                assert AB_embedding.check_edge2path()
                assert AB_embedding.check_vertex_disjointness()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()