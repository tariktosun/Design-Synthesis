'''
Created on Dec 29, 2013

@author: tariktosun
'''
from Embedding.Node import Node

class Design(object):
    '''
    A design, composed of nodes and edges.
    '''


    def __init__(self, root_node):
        '''
        Constructor
        '''
        # list of nodes in this design
        nodes = []
        edges = []
        self.parse_tree(root_node, nodes, edges)
        self.nodes = nodes
        # for now, the design just gets its edges from the nodes.
        self.edges = edges
        
    def parse_tree(self, root_node, nodes, edges):
        '''
        Extracts all nodes and edges from a connected set of nodes.
        '''
        assert not root_node in nodes, "Something is wrong!"
        nodes.append(root_node)
        if root_node.parent_edge:
            edges.append(root_node.parent_edge)
        for child in root_node.children:
            self.parse_tree(child, nodes, edges)
        return
            