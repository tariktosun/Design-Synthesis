'''
Created on Dec 29, 2013

@author: tariktosun
'''
#from Embedding.Node import Node

import Node

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