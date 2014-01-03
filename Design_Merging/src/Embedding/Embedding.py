'''
Created on Dec 30, 2013

@author: tariktosun
'''

import Design
from itertools import permutations
import numpy as np

class Embedding(object):
    '''
    Embedding class, specifying the way one design may embed another.
    '''


    def __init__(self, superD, subD, nodemap=None):
        '''
        Constructor
        '''
        assert isinstance(superD, Design.Design), 'Incorrect arguments for Embedding'
        assert isinstance(subD, Design.Design), 'Incorrect arguments for Embedding'
        if nodemap is not None:
            assert isinstance(nodemap, dict), 'Incorrect arguments for Embedding'
        
        self.A = superD
        self.B = subD
        
        # Initialize table for dynamic programming.
        self.T = { superN:{ subN:None for subN in self.B.nodes } 
                  for superN in self.A.nodes }
        
        self.nodemap = nodemap
        
    def check_topological_embedding_dynamic(self):
        '''
        Check topological embedding using dynamic programming algorithm.
        '''
        return self._embeds(self.A.root_node, self.B.root_node)
        
    def _embeds(self, superN, subN):
        '''
        Recursive function testing subtree embedding.
        '''
        # Recursively ensure that all child pairings have table entries:
        for superC in superN.children:
            for subC in subN.children:
                if self.T[superC][subC] == None:
                    self.T[superC][subC] = self._embeds(superC, subC)
                    #print superC.name + ', ' + subC.name
        
        # < Add a functionality check here >
        # < Add end effector check here >
        # check child matching using brute force enumeration:
        if len(superN.children)<len(subN.children):
            return False
        for sub_children_perm in permutations(subN.children):
            for super_children_perm in permutations(superN.children, len(subN.children)):
                # NOTE: all( [] ) evaluates to True.
                if all( self.T[z[0]][z[1]]==True for z in zip(super_children_perm, sub_children_perm) ):
                    # We have found an embedding. Propagate upwards.
                    p = superN.parent
                    while p is not None:
                        self.T[p][subN] = True
                        p = p.parent
                    #print [foo.values() for foo in self.T.values()]
                    return True
        return False
        
              
    def check_topological_embedding_brute(self):
        '''
        Brute-force combinatoric method to check topological embedding
        '''
        N = len(self.B.nodes) # number of subdesign nodes
        if len(self.A.nodes) < N:
            # shortcut - fewer nodes in superdesign
            self.nodemap = None
            return False
        for sub_perm in permutations(self.B.nodes):
            for super_perm in permutations(self.A.nodes, N):
                self.nodemap = dict (zip(sub_perm, super_perm))
                if self.check_vertex2vertex():
                    if self.check_edge2path():
                        if self.check_vertex_disjointness():
                            return True
        # no embedding found.
        self.nodemap = None
        return False
        
    def check_vertex2vertex(self):
        ''' 
        Returns True if nodemap satisfies vertex to vertex correspondence with A
        embedding B.
        map is a dict.
        '''
        nodemap = self.nodemap
        superD = self.A
        subD = self.B
        # ensure nodemap is valid:
        for i in nodemap.iteritems():
            assert i[0] in subD.nodes
            assert i[1] in superD.nodes
        # check that all nodes in B are present in map:
        used_nodes = []
        for node in subD.nodes:
            # all nodes must be present:
            if not nodemap.has_key(node):
                return False
            # mapped nodes must subsume functionality:
            #if not nodemap[node].type > node.type:
            #    return False
            # check one-to-oneness:
            if nodemap[node] in used_nodes:
                return False
            used_nodes.append(nodemap[node])
        return True
    
    def check_edge2path(self):
        '''
        Returns True if nodemap satisfies edge-to-path correspondence with A
        embedding B.
        '''
        #A = embedding.A
        subD = self.B
        nodemap = self.nodemap
        for edge in subD.edges:
            assert nodemap.has_key(edge.parent), 'Edge parent maps to no node in superdesign'
            super_parent = nodemap[edge.parent]
            assert nodemap.has_key(edge.child), 'Edge child maps to no node in superdesign'
            super_child = nodemap[edge.child]
            p = super_child.parent
            while p is not super_parent:
                if p is None:
                    return False    # root reached
                p = p.parent
        return True
            
    def check_vertex_disjointness(self):
        '''
        Returns True if nodemap is path-vertex disjoint, false otherwise.
        '''
        subD = self.B
        nodemap = self.nodemap
        used_nodes = []
        for edge in subD.edges:
            assert nodemap.has_key(edge.parent), 'Edge parent maps to no node in superdesign'
            super_parent = nodemap[edge.parent]
            assert nodemap.has_key(edge.child), 'Edge child maps to no node in superdesign'
            super_child = nodemap[edge.child]
            p = super_child.parent
            while p is not super_parent:
                assert p is not None, 'Edge does not map to a path in superdesign.'
                if p in used_nodes:
                    return False
                used_nodes.append(p)
                p = p.parent    # path parent not appended to used_nodes.
        return True