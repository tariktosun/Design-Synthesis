'''
Created on Dec 29, 2013

@author: tariktosun
'''
import unittest
import Embedding.Node as Node
import Embedding.Edge as Edge
import Embedding.Design as Design

class Test_Embedding(unittest.TestCase):
    
    
    def setUp(self):
        b = [0]*4
        a = [0]*6
        for i in xrange(len(b)):
            b[i] = Node.Node(str(i))
        for i in xrange(len(a)):
            a[i] = Node.Node(str(i))
        # build structure:
        b[3].add_child(b[2])
        b[2].add_child(b[1])
        b[2].add_child(b[0])
        
        a[5].add_child(a[4])
        a[4].add_child(a[3])
        a[4].add_child(a[2])
        a[3].add_child(a[1])
        a[2].add_child(a[0])
        
        # Store as class variables:
        self.B = Design.Design(b)
        self.A = Design.Design(a)
        self.nodemap = {b[0]:a[0],
                        b[1]:a[1],
                        b[2]:a[4],
                        b[3]:a[5],
                        }
        
    def tearDown(self):
        pass

    def test_vertex2vertex(self):
        assert self.check_vertex2vertex(self.nodemap, self.A, self.B)
        
        # test reverse:
        reversemap = dict (zip(self.nodemap.values(),self.nodemap.keys()))
        assert ~ self.check_vertex2vertex(reversemap, self.B, self.A)
        
    def check_vertex2vertex(self, nodemap, A, B):
        ''' 
        Returns True if nodemap satisfies vertex to vertex correspondence with A
        embedding B.
        map is a dict.
        '''
        # ensure nodemap is valid:
        for i in nodemap.iteritems():
            assert i[0] in B.nodes
            assert i[1] in A.nodes
        # check that all nodes in B are present in map:
        used_nodes = []
        for node in B.nodes:
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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()