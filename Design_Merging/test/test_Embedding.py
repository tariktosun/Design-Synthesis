'''
Created on Dec 29, 2013

@author: tariktosun
'''
import unittest
import Embedding.Node as Node
import Embedding.Edge as Edge
import Embedding.Design as Design
import Embedding.Embedding as Embedding

class Test_Embedding(unittest.TestCase):
    
    
    def setUp(self):
        ''' define fixtures for tests. '''
        sub = [0]*4
        sup = [0]*6
        for i in xrange(len(sub)):
            sub[i] = Node.Node(str(i))
        for i in xrange(len(sup)):
            sup[i] = Node.Node(str(i))
        # build structure:
        sub[3].add_child(sub[2])
        sub[2].add_child(sub[1])
        sub[2].add_child(sub[0])
        
        sup[5].add_child(sup[4])
        sup[4].add_child(sup[3])
        sup[4].add_child(sup[2])
        sup[3].add_child(sup[1])
        sup[2].add_child(sup[0])
        
        # Store as class variables:
        self.subD = Design.Design(sub[3])
        self.superD = Design.Design(sup[5])
        self.nodemap = {sub[0]:sup[0],
                        sub[1]:sup[1],
                        sub[2]:sup[4],
                        sub[3]:sup[5],
                        }
        
    def tearDown(self):
        pass

    def test_edge2path(self):
        assert self.check_edge2path(self.nodemap, self.superD, self.subD)

    def test_vertex2vertex(self):
        # pass set:
        pass_set = []
        pass_set.append(Embedding(self.nodemap, self.superD, self.subD))
        # fail set:
        fail_set = []
        # test reverse:
        reversemap = dict (zip(self.nodemap.values(),self.nodemap.keys()))
        fail_set.append(Embedding(reversemap, self.subD, self.superD))
        
        # STOPPED HERE: need to make check functions take embeddings, and wrap these checks in a for loop.
        assert self.check_vertex2vertex(self.nodemap, self.superD, self.subD)
        
        
        assert ~ self.check_vertex2vertex(reversemap, self.subD, self.superD)
        
    def check_vertex2vertex(self, nodemap, superD, subD):
        ''' 
        Returns True if nodemap satisfies vertex to vertex correspondence with superD
        embedding subD.
        map is a dict.
        '''
        # ensure nodemap is valid:
        for i in nodemap.iteritems():
            assert i[0] in subD.nodes
            assert i[1] in superD.nodes
        # check that all nodes in subD are present in map:
        used_nodes = []
        for node in subD.nodes:
            # all nodes must be present:
            if not nodemap.has_key(node):
                return False
            # mapped nodes must subsume functionality:
            #if not nodemap[node].type > node.type:
            #    return False
            # check one-to-oneness:
            if nodemap[node] in used_nodes:
                return False
            used_nodes.append(nodemap[node])
        return True
    
    def check_edge2path(self, nodemap, superD, subD):
        '''
        Returns True if nodemap satisfies edge-to-path correspondence with superD
        embedding subD.
        '''
        for edge in subD.edges:
            super_parent = nodemap[edge.parent]
            super_child = nodemap[edge.child]
            p = super_child.parent
            while p is not super_parent:
                if p is None:
                    return False    # root reached
                p = p.parent
        return True
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()