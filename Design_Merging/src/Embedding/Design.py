'''
Created on Dec 29, 2013

@author: tariktosun
'''
from Embedding.Node import Node

class Design(object):
    '''
    A design, composed of nodes and edges.
    '''


    def __init__(self, nodes):
        '''
        Constructor
        '''
        # list of nodes in this design
        self.nodes = nodes