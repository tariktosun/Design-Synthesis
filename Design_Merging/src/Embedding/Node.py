'''
Created on Dec 28, 2013

@author: tariktosun
'''
from Embedding.Edge import Edge

class Node(object):
    '''
    Node class for design merging
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # List of pointers to child nodes
        self.children = []
        # Edge linking this node to its parent
        self.parent_edge = None
        # Pointer to parent node
        self.parent = None
        # Type abstractly captures functionality (for now)
        self.type = None
    
    def nodecost(self):
        '''
        Returns the cost of this node.
        '''
        pass
    
    def add_child(self, child, length):
        '''
        Builds an edge of specified length from child to this node, making it a
        child of this node.
        '''
        self.children.append(child)
        e = Edge(self, child, length)
        child.parent = self
        child.parent_edge = e
        return
        
    def remove_child(self, child):
        '''
        Breaks edge between this node and child.
        '''        
        if child in self.children:
            self.children.remove(child)
        else:
            raise Exception('Child removal failed.  Node was not in list of children.')
        if child.parent == self:
            child.parent = None
            child.parent_edge = None
            # Note: edge is now orphaned.
        else:
            raise Exception('Child removal failed.  Node was not child\'s parent.')
        