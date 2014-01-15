'''
Created on Jan 15, 2014

@author: tariktosun
'''
import unittest
import Embedding.Node as Node
import Embedding.Design as Design
from Embedding import Embedding

class Test_Smores(unittest.TestCase):


    def setUp(self):
        ''' sets up fixtures. '''
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
        a[3].parent_edge.length = 0
        

    def tearDown(self):
        pass

    def test_stripping_simple(self):
        ''' Simple test of node stripping. '''
        stripped_B = self.B.strip_inactive_nodes()
        assert len(stripped_B.nodes) == 4
        assert len(self.B.nodes) == 8
        assert len(stripped_B.edges) == 3
        assert len(self.B.edges) == 7
        
    def test_manual_smores_embedding(self):
        '''
        Tests embedding after node stripping using two simple, manually created
        SMORES-like designs.
        '''
        stripped_B = self.B.strip_inactive_nodes()
        stripped_embedding = Embedding.Embedding(self.A, stripped_B, self.params)
        unstripped_embedding = Embedding.Embedding(self.A, self.B, self.params)
        
        # dynamic & brute embeddings of stripped version should both pass:
        #brute
        assert stripped_embedding.check_topological_embedding_brute()
        assert stripped_embedding.check_vertex2vertex()
        assert stripped_embedding.check_edge2path()
        assert stripped_embedding.check_vertex_disjointness()
        # dynamic:
        assert stripped_embedding.check_topological_embedding_dynamic()
        assert stripped_embedding.check_vertex2vertex()
        assert stripped_embedding.check_edge2path()
        assert stripped_embedding.check_vertex_disjointness()
        
        
        # dynamic & brute of unstripped version should both fail.
        #brute
        #print "beginning unstripped brute"
        #assert not unstripped_embedding.check_topological_embedding_brute()
        # dynamic:
        #print "beginning unstripped dynamic"
        assert not unstripped_embedding.check_topological_embedding_dynamic()
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()