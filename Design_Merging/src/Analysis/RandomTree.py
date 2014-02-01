'''
RandomTree.py
Created on Feb 1, 2014

@author: tarik
'''

import Embedding.Node as Node
import Embedding.Design as Design
from random import randint

class RandomTree(Design.Design):
    ''' A random tree design for testing.'''
    def __init__(self, branching_factor, max_depth):
        ''' Constructor '''
        root_node = Node.Node('root')
        root_node.type = 1  # All nodes are type 1.
        self.branching_factor = branching_factor
        self.max_depth = max_depth
        self.nodes = [root_node]
        self.grow_tree( root_node, 1)   # sets the self.nodes attribute.
        # parse the tree:
        nodes = []
        edges = []
        self.parse_tree(root_node, nodes, edges)
        assert set(self.nodes) == set(nodes), 'Mismatch in tree and node_list'
        self.edges = edges
        self.root_node = root_node
        # determine avg branching factor:
        N = 0.0
        C = 0.0
        for n in self.nodes:
            if n.children == []:
                continue    # don't count leaves.
            N +=1
            C += len(n.children)
        if C >0:
            self.average_branching_factor = N/C
        else:
            self.average_branching_factor = 0  
        

    def grow_tree(self, root_node, current_depth):
        '''
        Recursive function that grows the tree
        '''
        assert current_depth <= self.max_depth, 'Tree grew beyond max depth.'
        if current_depth == self.max_depth:
            return
        children = [Node.Node('noname') for _ in xrange(randint(0,self.branching_factor))]
        for c in children:
            c.type = 1  # all nodes are type 1
            root_node.add_child(c)
            self.nodes.append(c)
            # recurse:
            self.grow_tree(c, current_depth+1)
        return

if __name__ == '__main__':
    pass