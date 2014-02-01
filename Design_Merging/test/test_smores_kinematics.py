'''
Created on Jan 31, 2014

@author: tarik
'''
import unittest
#import Embedding.Node as Node
#import Embedding.Design as Design
from Embedding import Embedding
import Embedding.SmoresModule as SmoresModule
import Embedding.SmoresDesign as SmoresDesign
from fixtures_kinematic_grasper_walker import setUpKinematicGrasperWalker

class Test_Smores_Kinematics(unittest.TestCase):


    def setUp(self):
        '''
        sets up fixtures.
        '''
        # Type subsumption:
        types_subsumed = {1: [1,2], 2: [2]}
        length_scaling = 1
        self.params = {'types_subsumed': types_subsumed,
                       'length_scaling': length_scaling}
        
        ''' The same designs, but made using the SmoresModule class: '''
        # Subdesign:
        b_smores = [ SmoresModule.SmoresModule('B0',4, [2,3]), SmoresModule.SmoresModule('B1',0, [2,3]) ]
        # build structure:
        b_smores[1].add_child_module( 4, b_smores[0] )
        # make a SmoresDesign and store :
        self.BSmores = SmoresDesign.SmoresDesign( b_smores[1], b_smores )
        
        # Superdesign:
        a_smores = [ SmoresModule.SmoresModule( 'A0', 4 ), SmoresModule.SmoresModule( 'A1', 2, [4] ) ]
        # build structure:
        a_smores[1].add_child_module( 3 , a_smores[0] )
        # make a SmoresDesign and store it:
        self.ASmores = SmoresDesign.SmoresDesign( a_smores[1], a_smores )
        
        # nodemaps:
        self.AB_nodemap = {b_smores[1].nodes[0]: a_smores[1].nodes[2],
                           b_smores[1].nodes[1]: a_smores[1].nodes[1],
                           b_smores[1].nodes[4]: a_smores[1].nodes[3],
                           b_smores[0].nodes[1]: a_smores[0].nodes[1],
                           b_smores[0].nodes[0]: a_smores[0].nodes[0],
                           } #no - actually doesn't work with kinematics!

        ''' Grasper and walker: '''
        setUpKinematicGrasperWalker(self)


    def tearDown(self):
        pass
    def test_stripping_simple(self):
        ''' Simple test of node stripping. '''
        assert len(self.BSmores.nodes) == 9
        assert len(self.BSmores.edges) == 8
        
        self.BSmores.strip_inactive_nodes()
        assert len(self.BSmores.nodes) == 5
        assert len(self.BSmores.edges) == 4
        
     
    def test_smores_class_kinematics(self):
        '''
        Tests a pre-defined nodemap for BSmores and ASmores.
        '''
        self.BSmores.strip_inactive_nodes()
        stripped_embedding = Embedding.Embedding(self.ASmores, self.BSmores, self.params, self.AB_nodemap)
        assert stripped_embedding.check_vertex2vertex()
        assert not stripped_embedding.check_edge2path()
        assert stripped_embedding.check_vertex_disjointness()
    
    def test_smores_class_embedding(self):
        '''
        The same as test_manual_smores_embedding, but with the SMORES class nodes.
        '''
        #stripped_BSmores = self.BSmores.strip_inactive_nodes()
        # note that A has not been stripped yet.
        self.BSmores.strip_inactive_nodes()
        stripped_embedding = Embedding.Embedding(self.ASmores, self.BSmores, self.params)
        #unstripped_embedding = Embedding.Embedding(self.ASmores, self.BSmores, self.params)
        
        # dynamic & brute embeddings of stripped version should both pass:
        '''
        #brute
        assert stripped_embedding.check_kinematic_embedding_brute()
        assert stripped_embedding.check_vertex2vertex()
        assert stripped_embedding.check_edge2path()
        assert stripped_embedding.check_vertex_disjointness()
        '''
        # dynamic:
        assert not stripped_embedding.check_kinematic_embedding_dynamic()
    
        # only dynamic because brute takes too long to run.
        #assert not unstripped_embedding.check_topological_embedding_dynamic()
    
    def test_small_grasper_walker(self):
        '''
        Tests only the small part of the walker and grasper.
        '''
        self.small_grasper.strip_inactive_nodes()
        gInW_small_embedding = Embedding.Embedding(self.small_walker, self.small_grasper, self.params, self.WG_small_nodemap)
        
        #assert gInW_embedding.check_kinematic_embedding_dynamic()
        assert gInW_small_embedding.check_vertex2vertex()
        assert gInW_small_embedding.check_edge2path()
        assert gInW_small_embedding.check_vertex_disjointness()
    
    def test_grasper_walker(self):
        '''
        Tests embedding the grasper in the walker.
        '''
        self.grasper.strip_inactive_nodes()
        gInW_embedding = Embedding.Embedding(self.walker, self.grasper, self.params, self.WG_nodemap)
        
        #assert gInW_embedding.check_kinematic_embedding_dynamic()
        assert gInW_embedding.check_vertex2vertex()
        assert gInW_embedding.check_edge2path()
        assert gInW_embedding.check_vertex_disjointness()
      
    """    
    def test_grasper_walker_brute(self):
        '''
        Test dynamic programming grasper walker.
        '''
        self.grasper.strip_inactive_nodes()
        gInW_embedding = Embedding.Embedding(self.walker, self.grasper, self.params)
        
        assert gInW_embedding.check_kinematic_embedding_brute()
        assert gInW_embedding.check_vertex2vertex()
        assert gInW_embedding.check_edge2path()
        assert gInW_embedding.check_vertex_disjointness()
    """
     
    def test_grasper_walker_dynamic(self):
        '''
        Test dynamic programming grasper walker.
        '''
        self.grasper.strip_inactive_nodes()
        gInW_embedding = Embedding.Embedding(self.walker, self.grasper, self.params)
        
        assert gInW_embedding.check_kinematic_embedding_dynamic()
        assert gInW_embedding.check_vertex2vertex()
        assert gInW_embedding.check_edge2path()
        assert gInW_embedding.check_vertex_disjointness()
        nicenames = {k.name: v.name for (k,v) in gInW_embedding.AB_nodemap.items()}
        print nicenames
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()