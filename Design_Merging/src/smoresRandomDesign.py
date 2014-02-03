'''
RandomTree.py
Created on Feb 1, 2014

@author: tarik
'''

import Embedding.Node as Node
import Embedding.SmoresModule as SmoresModule
import Embedding.SmoresDesign as SmoresDesign
from random import randint
from random import choice

class SmoresRandomDesign(SmoresDesign.SmoresDesign):
    ''' A random tree design for testing.'''
    def __init__(self, branching_factor, depth):
        ''' Constructor '''
        
        root_module = SmoresModule.SmoresModule('root', choice([0,2,3,4]))
        self.branching_factor = branching_factor
        self.depth = depth
        self.modules = [root_module]
        self.grow_tree(root_module, 1)
        
        # now for normal constructor stuff:
        self.nodes = []
        for m in self.modules:
            self.nodes += m.nodes
        # remove duplicates from merging:
        self.nodes = list(set(self.nodes))
        # parse the underlying node tree:
        root_node = root_module.nodes[root_module.root_node_number]
        nodes = []
        edges= []
        self.parse_tree(root_node, nodes, edges)
        # ensure node_list and nodes have the same nodes:
        assert set(self.nodes) == set(nodes), 'Mismatch in tree and node_list'
        self.edges = edges
        self.root_node = root_node
        self.root_module = root_module
        
    
    def grow_tree(self, root_module, current_depth):
        ''' Recursive function that grows the module tree. '''
        assert current_depth <= self.depth, 'Tree grew beyond max depth.'
        if current_depth == self.depth:
            if self.is_subdesign:
                # leave only one active node at the end.
                available_nodes = [0,2,3,4]
                available_nodes.remove(choice(available_nodes))
                for i in available_nodes:
                    root_module.nodes[i].active = False
            return
        child_modules = [SmoresModule.SmoresModule('noname', choice([0,2,3,4])) for _ in xrange(randint(0, self.branching_factor))]
        available_nodes = [0,2,3,4]
        for c in child_modules:
            node_number = choice(available_nodes)
            available_nodes.remove(node_number)
            root_module.add_child_module(node_number, c)
            self.modules.append(c)
            self.grow_tree(c, current_depth+1)
        if self.is_subdesign:
            # any nodes still available are marked inactive.
            for i in available_nodes:
                root_module.nodes[i].active = False
        return

if __name__ == '__main__':
    pass