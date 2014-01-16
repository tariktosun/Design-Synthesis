'''
Created on Jan 15, 2014

@author: tariktosun
'''
import unittest
import Embedding.Node as Node
import Embedding.Design as Design
from Embedding import Embedding
import Embedding.SmoresModule as SmoresModule
import Embedding.SmoresDesign as SmoresDesign

class Test_Smores(unittest.TestCase):


    def setUp(self):
        '''
        sets up fixtures.
        '''
        
        ''' Manually created SMORES designs: '''
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
        self.B.nodes[3].parent_edge.length = 2
        
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
        #a[3].parent_edge.length = 0 incorrect.
        
        ''' The same designs, but made using the SmoresModule class: '''
        # Subdesign:
        b_smores = [ SmoresModule.SmoresModule('0',1, [2,3]), SmoresModule.SmoresModule('1',0, [2,3]) ]
        # build structure:
        b_smores[1].add_child_module( 1, b_smores[0] )
        # make a SmoresDesign and store :
        self.BSmores = SmoresDesign.SmoresDesign( b_smores[1], b_smores )
        
        # Superdesign:
        a_smores = [ SmoresModule.SmoresModule( '0', 1 ), SmoresModule.SmoresModule( '1', 2 ) ]
        # build structure:
        a_smores[1].add_child_module( 3 , a_smores[0] )
        # make a SmoresDesign and store it:
        self.ASmores = SmoresDesign.SmoresDesign( a_smores[1], a_smores )

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
        # Note: this takes far too long to run!
        # dynamic:
        #print "beginning unstripped dynamic"
        assert not unstripped_embedding.check_topological_embedding_dynamic()
        
    def test_smores_class_basic(self):
        '''
        Basic test of the smores class.  Tests for equality with the manually
        created designs by checking that each embeds the other.
        '''
        #B_in_B = Embedding.Embedding(self.B, self.B, self.params)
        B_in_BSmores = Embedding.Embedding(self.BSmores, self.B, self.params)
        BSmores_in_B = Embedding.Embedding(self.B, self.BSmores, self.params)
        A_in_ASmores = Embedding.Embedding(self.ASmores, self.A, self.params)
        ASmores_in_A = Embedding.Embedding(self.A, self.ASmores, self.params)
        
        embeddings = [B_in_BSmores, BSmores_in_B, A_in_ASmores, ASmores_in_A]
        for i,e in enumerate(embeddings):
            assert e.check_topological_embedding_dynamic(), str(i)
            assert e.check_vertex2vertex(), str(i)
            assert e.check_edge2path(), str(i)
            assert e.check_vertex_disjointness(), str(i)
            
    def test_smores_class_embedding(self):
        '''
        The same as test_manual_smores_embedding, but with the SMORES class nodes.
        '''
        stripped_BSmores = self.BSmores.strip_inactive_nodes()
        stripped_embedding = Embedding.Embedding(self.ASmores, stripped_BSmores, self.params)
        unstripped_embedding = Embedding.Embedding(self.ASmores, self.BSmores, self.params)
        
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
        
        # only dynamic because brute takes too long to run.
        assert not unstripped_embedding.check_topological_embedding_dynamic()
            
            
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()