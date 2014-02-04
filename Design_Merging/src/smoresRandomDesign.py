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
    def __init__(self, branching_factor, num_modules, min_depth, is_subdesign=False):
        ''' Constructor '''
        
        self.is_subdesign = is_subdesign
        self.branching_factor = branching_factor
        self.num_modules = num_modules
        self.min_depth = min_depth
        
        while True:
            # continue until we generate an appropriate tree
            root_module = SmoresModule.SmoresModule('root', choice([0,2,3,4]))
            self.modules = [root_module]
            self.grow_tree(root_module, 1, 1)
            if len(self.modules)==self.num_modules:
                break
            print 'restarting'
        
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
        self.check_validity()
        
        
    def check_validity(self):
        ''' performs some checks to ensure this design is valid. '''
        assert len(self.modules) == self.num_modules
        # determine avg branching factor:
        N = 0.0
        C = 0.0
        for m in self.modules:
            num_child_modules = sum([c is not None for c in m.child_modules])
            assert num_child_modules<=self.branching_factor
            assert num_child_modules>=0
            if m.child_modules == []:
                continue    # don't count leaves.
            N +=1
            C += num_child_modules
        if C >0:
            average_branching_factor = N/C
        else:
            average_branching_factor = 0
        #print "average branching factor: " + str(average_branching_factor)
         
        
        
    def grow_tree(self, root_module, current_num_modules, current_depth):
        ''' Recursive function that grows the module tree. '''
        assert current_num_modules <= self.num_modules, 'Tree grew beyond max size.'
        num_descendants = 0    
        available_nodes = [0,2,3,4]
        available_nodes.remove(root_module.root_node_number)
        if current_num_modules == self.num_modules:
            if self.is_subdesign:
                # leave only one active node at the end.
                available_nodes.remove(choice(available_nodes))
                for i in available_nodes:
                    root_module.nodes[i].active = False
            return 0
        if current_depth < self.min_depth:
            min_branch = 1
        else:
            min_branch = 0
        child_modules = [SmoresModule.SmoresModule('noname', choice([0,2,3,4])) for _ in xrange(randint(min_branch, self.branching_factor))]
        for c in child_modules:
            if current_num_modules + num_descendants == self.num_modules:
                return num_descendants
            num_descendants += 1
            node_number = choice(available_nodes)   # Add to a random available node
            available_nodes.remove(node_number)
            root_module.add_child_module(node_number, c)
            self.modules.append(c)
            nd = self.grow_tree(c, current_num_modules + num_descendants, current_depth + 1)
            num_descendants += nd
        if self.is_subdesign:
            # any nodes still available are marked inactive.
            for i in available_nodes:
                root_module.nodes[i].active = False
        return num_descendants
    

if __name__ == '__main__':
    pass