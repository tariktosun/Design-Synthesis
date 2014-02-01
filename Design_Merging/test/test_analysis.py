'''
Created on Feb 1, 2014

@author: tarik
'''
import unittest
import Embedding.Node as Node
import Embedding.Design as Design
from Embedding import Embedding
from Analysis.RandomTree import RandomTree

class TestAnalysis(unittest.TestCase):


    def setUp(self):
        ''' set up fixtures for tests. '''
        pass


    def tearDown(self):
        pass


    def test_RandomTree(self):
        ''' Tests that the GrowRandomTree function is behaving properly. '''
        r = RandomTree(4, 1)
        assert len(r.nodes) == 1
        for i in xrange(100):
            r = RandomTree(4,2)
            assert len(r.root_node.children)<=4
            assert len(r.nodes) <= 5
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()