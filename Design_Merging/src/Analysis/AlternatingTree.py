'''
Created on Feb 1, 2014

@author: tariktosun
'''

import Embedding.Node as Node
import Embedding.Design as Design
from random import randint

class AlternatingTree(Design.Design):
    '''
    Creates trees for the alternating tree test.  Can create a tree of specified
    depth and branching factor with alternating node types, or with random node 
    types.
    '''

    def __init__(self, tree_type, branching_factor, depth):
        '''
        Constructor
        '''
        root_node = Node.Node('root')
        self.branching_factor = branching_factor
        self.depth = depth
        self.nodes = [root_node]
        # grow the tree:
        if tree_type=='random':
            root_node.type = randint(1,2)
            self.grow_random(root_node, 1)
        elif tree_type=='alternating':
            assert depth % 2 == 0, 'Depth must be even for alternating tree'
            root_node.type = 1
            self.grow_alternating(root_node, 1)
        else:
            assert False, 'Invalid type'
        # parse the tree:
        nodes = []
        edges = []
        self.parse_tree(root_node, nodes, edges)
        assert set(self.nodes) == set(nodes), 'Mismatch in tree and node_list'
        self.edges = edges
        self.root_node = root_node
    
    def grow_alternating(self, root_node, current_depth):
        ''' Grows an alternating tree '''
        assert current_depth <= self.depth, 'Tree grew beyond max depth'
        if current_depth == self.depth:
            return
        children = [Node.Node('noname') for _ in xrange(self.branching_factor)]
        # determine type:
        if root_node.type == 1:
            child_type = 2
        elif root_node.type == 2:
            child_type = 1
        else:
            assert False, 'Invalid root_node type.'
        for c in children:
            c.type = child_type
            root_node.add_child(c)
            self.nodes.append(c)
            # recurse:
            self.grow_alternating(c, current_depth+1)
        return
    
    def grow_random(self, root_node, current_depth):
        ''' Grows a tree with random type assignment. '''
        assert current_depth <= self.depth, 'Tree grew beyond max depth'
        if current_depth == self.depth:
            return
        children = [Node.Node('noname') for _ in xrange(self.branching_factor)]
        for c in children:
            c.type = randint(1,2)
            root_node.add_child(c)
            self.nodes.append(c)
            # recurse:
            self.grow_random(c, current_depth+1)
        return
        
        
        
        
        