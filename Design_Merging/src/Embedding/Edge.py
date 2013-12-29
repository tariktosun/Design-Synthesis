'''
Created on Dec 28, 2013

@author: tariktosun
'''

class Edge(object):
    '''
    Edge class for design embedding.
    '''


    def __init__(self, parent, child, length):
        '''
        parent and child are Nodes.
        '''
        # The parent node
        self.parent = parent
        # The child node
        self.child = child
        # Edge length
        self.length = length