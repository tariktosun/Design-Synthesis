'''
Created on Dec 30, 2013

@author: tariktosun
'''

import Design
from itertools import permutations
import numpy as np
import pandas

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
        
        self.superD = superD
        self.subD = subD
        
        # Initialize table for dynamic programming.
        self.T = { superN:{ subN:None for subN in self.subD.nodes } 
                  for superN in self.superD.nodes }
        
        self.nodemap = nodemap
        
    def pretty_nodemap(self, nodemap=-1):
        '''
        Pretty-print the nodemap.
        '''
        if nodemap==-1:  # hack to produce default behavior.
            return {k.name:v.name for k,v in self.nodemap.iteritems()}
        elif type(nodemap) is dict:
            return {eval(k.name):eval(v.name) for k,v in nodemap.iteritems()}
        else:
            return nodemap
            
        
    def pretty_T(self):
        '''
        Pretty-print the table T
        '''
        super_names = [N.name for N in self.superD.nodes]
        sub_names = [N.name for N in self.subD.nodes]
        T_list = [[self.pretty_nodemap(self.T[superN][subN]) for subN in self.subD.nodes]
                   for superN in self.superD.nodes]
        #T_list = [[self.pretty_nodemap(vv) for vv in v.itervalues()] for v in self.T.itervalues()]
        return pandas.DataFrame(T_list, super_names, sub_names)
        #print {k.name:{kk.name:vv  for kk,vv in v.iteritems()} for k,v in self.T.iteritems()}     
        
    def check_topological_embedding_dynamic(self):
        '''
        Check topological embedding using dynamic programming algorithm.
        '''
        boolean_result = self._embeds(self.superD.root_node, self.subD.root_node)
        self.nodemap = self.T[self.superD.root_node][self.subD.root_node]
        return boolean_result
        
    def _embeds(self, superN, subN):
        '''
        Recursive function testing subtree embedding.
        '''
        if superN.children == [] and subN.children == []:
            ''' base case 1: nodes with no children.
            Embeds if:
                subN may map to superN.
            '''
            
            
            
            # < Add functionality check here >
        
            # < Add end-effector check here >
            
            # We have found an embedding. Record it and propagate upwards:
            nodemap = {subN:superN}
            self.T[superN][subN] = nodemap
            p = superN.parent
            while p is not None:
                self.T[p][subN] = nodemap
                p = p.parent
            return True
        elif subN.children == []:
            ''' base case 2: superN has children, but subN does not.
            Embeds if:
                (1) subN may embed in a child of superN
                (2) subN may map to superN
            '''
            
            ''' (1) Does subN embed in a child of superN? '''
            # Recursively ensure that all pairs of subN with children of superN
            # have table entries:
            for superC in superN.children:
                if self.T[superC][subN] == None:
                    self._embeds(superC, subN)
            # return True if an embedding in a child was found (and propagated up)
            if type(self.T[superN][subN]) == dict:
                return True
            
            ''' (2) Does subN map to superN? '''
            # < Add functionality check here >
            
            # < Add end-effector check here >
            
            # all tests passed, so we have found a root-matched embedding.
            # all children of superN in this case MUST be unused (subN is a leaf)
            nodemap = {subN:superN}
            self.T[superN][subN] = nodemap
            # propagate to parents:
            p = superN.parent
            while p is not None:
                self.T[p][subN] = nodemap
                p = p.parent
            #return
            return True
        elif superN.children == []:
            ''' if superN has no children but subN has children, superN cannot
            possibly embed subN. '''
            self.T[superN][subN] = False
            return False   
        else:
            ''' non-base case: Both subN and superN have children.
            Embeds if:
                (1) subN may embed in a child of superN
                (2) A matching may be found between the children of subN and superN,
                    and subN may map to superN.
            '''
                  
            ''' (1) does subN embed in a child of superN? '''
            # Recursively ensure that all pairs of subN with children of superN
            # have table entries:
            for superC in superN.children:
                if self.T[superC][subN] == None:
                    self._embeds(superC, subN)
            # return True if an embedding in a child was found (and propagated up)
            if type(self.T[superN][subN]) == dict:
                return True
            
            ''' (2) Can a matching be found between children of subN and superN,
                    and can subN map to superN? ''' 
            # Recursively ensure that all child pairings have table entries:
            for superC in superN.children:
                for subC in subN.children:
                    if self.T[superC][subC] == None:
                        #self.T[superC][subC] = self._embeds(superC, subC)
                        self._embeds(superC, subC)
            
            # < Add a functionality check here >
            
            # < Add end effector check here >
            
            # check child matching using brute force enumeration:
            if len(superN.children)<len(subN.children):
                # if superN has fewer children than subN, vertex-disjoint embedding is impossible.
                self.T[superN][subN] = False
                return False
            #brute force search for matching:
            for sub_children_perm in permutations(subN.children):
                for super_children_perm in permutations(superN.children, len(subN.children)):
                    # NOTE: all() evaluates to True if arg is not False or None.
                    # NOTE: all( [] ) evaluates to True.
                    if all( type(self.T[sup][sub])==dict for sup,sub in zip(super_children_perm, sub_children_perm) ):
                        # We have found an embedding. Record it and propagate upwards.
                        # Merge nodemaps of all child pairings in table:
                        nodemap = []
                        for sup,sub in zip(super_children_perm, sub_children_perm):
                            child_nodemap = self.T[sup][sub]
                            nodemap += child_nodemap.items()
                        nodemap = dict( nodemap )
                        # add in the parent pairing:
                        nodemap[subN] = superN                        
                        self.T[superN][subN] = nodemap
                        # propagate to parents:
                        p = superN.parent
                        while p is not None:
                            self.T[p][subN] = nodemap
                            p = p.parent
                        return True
            # children cannot be matched; embedding fails.
            self.T[superN][subN] = False
            return False
        
              
    def check_topological_embedding_brute(self):
        '''
        Brute-force combinatoric method to check topological embedding
        '''
        N = len(self.subD.nodes) # number of subdesign nodes
        if len(self.superD.nodes) < N:
            # shortcut - fewer nodes in superdesign
            self.nodemap = None
            return False
        for sub_perm in permutations(self.subD.nodes):
            for super_perm in permutations(self.superD.nodes, N):
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
        superD = self.superD
        subD = self.subD
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
        subD = self.subD
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
        subD = self.subD
        nodemap = self.nodemap
        used_nodes = []
        for edge in subD.edges:
            assert nodemap.has_key(edge.parent), 'Edge parent maps to no node in superdesign'
            super_parent = nodemap[edge.parent]
            assert nodemap.has_key(edge.child), 'Edge child maps to no node in superdesign'
            super_child = nodemap[edge.child]
            p = super_child
            while p is not super_parent:
                assert p is not None, 'Edge does not map to a path in superdesign.'
                if p in used_nodes:
                    return False
                used_nodes.append(p)
                p = p.parent    # path parent not appended to used_nodes.
        return True