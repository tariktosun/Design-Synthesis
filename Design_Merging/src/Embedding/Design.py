'''
Created on Dec 29, 2013

@author: tariktosun
'''
#from Embedding.Node import Node

import Node
import copy

class Design(object):
    '''
    A design, composed of nodes and edges.
    '''

    def __init__(self, root_node, node_list):
        '''
        Constructor
        '''
        assert isinstance(root_node, Node.Node)
        
        # list of nodes in this design
        self.nodes = node_list
        # parse tree to extract edges and ensure design is valid.
        nodes = []
        edges = []
        self.parse_tree(root_node, nodes, edges)
        # ensure node_list and nodes have the same nodes:
        assert set(self.nodes) == set(nodes), 'Mismatch in tree and node_list'
        # for now, the design just gets its edges from the nodes.
        self.edges = edges
        self.root_node = root_node
        
    def parse_tree(self, root_node, nodes, edges):
        '''
        Extracts all nodes and edges from a connected set of nodes.
        '''
        assert not root_node in nodes, "Design tree is invalid."
        nodes.append(root_node)
        if root_node.parent_edge:
            edges.append(root_node.parent_edge)
        for child in root_node.children:
            self.parse_tree(child, nodes, edges)
        return
    
    def strip_inactive_nodes(self):
        '''
        Returns a design identical to this one, but with inactive nodes stripped.
        Note that this does not modify the current Design, it returns a new one.
        '''
        stripped_design = copy.deepcopy(self)
        inactive_nodes = [n for n in stripped_design.nodes if n.active == False]
        for n in inactive_nodes:
            assert n.is_end_effector == False, 'Attempted to strip an inactive node that was an end effector'
            assert n.children == [], 'Attempted to strip inactive node ' + str(n.name) + ', but it had children'
            stripped_design.edges.remove(n.parent_edge)
            stripped_design.nodes.remove(n)
            p = n.parent
            p.remove_child(n)
        return stripped_design