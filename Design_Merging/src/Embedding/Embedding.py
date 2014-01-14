'''
Created on Dec 30, 2013

@author: tariktosun
'''

import Design
from itertools import permutations
import pandas

class Embedding(object):
    '''
    Embedding class, specifying the way one design may embed another.
    '''

    def __init__(self, superD, subD, params, nodemap=None):
        '''
        Constructor
        '''
        types_subsumed = params['types_subsumed']
        length_scaling = params['length_scaling']
        assert isinstance( superD, Design.Design ), 'Incorrect arguments for Embedding'
        assert isinstance( subD, Design.Design ), 'Incorrect arguments for Embedding'
        assert isinstance( types_subsumed, dict ), 'Incorrect arguments for Embedding'
        assert isinstance( length_scaling, (int, long, float) ), 'Incorrect arguments for Embedding'
        if nodemap is not None:
            assert isinstance(nodemap, dict), 'Incorrect arguments for Embedding'
        
        self.superD = superD
        self.subD = subD
        self.types_subsumed = types_subsumed
        self.valid_types = types_subsumed.keys()
        self.length_scaling = length_scaling
        
        # Initialize table for dynamic programming.
        self.T = { superN:{ subN:None for subN in self.subD.nodes } 
                  for superN in self.superD.nodes }
        
        self.AB_nodemap = nodemap
        
    def pretty_nodemap(self, nodemap=-1):
        '''
        Pretty-print the AB_nodemap.
        '''
        if nodemap==-1:  # hack to produce default behavior.
            return {k.name:v.name for k,v in self.AB_nodemap.iteritems()}
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
        
    def type_subsumes(self, supertype, subtype):
        '''
        Returns True if supertype subsumes subtype according to
        self.types_subsumed, False otherwise.
        '''
        assert supertype in self.valid_types, 'Type ' + str(supertype) + ' is invalid.'
        return subtype in self.types_subsumed[supertype]
        
    def node_subsumes(self, superN, subN):
        '''
        Returns True if superN may subsume subN, False otherwise.
        Checks functionality and end effector.
        '''
        # functionality check:
        if not self.type_subsumes(superN.type, subN.type):
            return False
        # end-effector check:
        if subN.is_end_effector:
            if not superN.is_end_effector:
                return False
            if not superN.children == []:
                return False
        return True    
        
    def check_topological_embedding_dynamic(self):
        '''
        Check topological embedding using dynamic programming algorithm.
        '''
        boolean_result = self._embeds(self.superD.root_node, self.subD.root_node)
        if boolean_result:
            # take the first valid embedding stored at the root.
            (length, root, nodemap) = self.T[self.superD.root_node][self.subD.root_node][0]
            self.AB_nodemap = nodemap
        else:
            self.AB_nodemap = False
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
            
            # functionality and end-effector check:
            if not self.node_subsumes(superN, subN):
                return False
            
            # We have found an embedding. Record it and propagate upwards:
            nodemap = {subN:superN}
            self._record_and_propagate(superN, subN, nodemap)
            
            #             nodemap = {subN:superN}
            #             self.T[superN][subN] = nodemap
            #             p = superN.parent
            #             while p is not None:
            #                 self.T[p][subN] = nodemap
            #                 p = p.parent
            
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
            #if type(self.T[superN][subN]) == dict:
            if type(self.T[superN][subN]) == list:
                return True
            
            ''' (2) Does subN map to superN? '''
            
            # functionality and end-effector check:
            if not self.node_subsumes(superN, subN):
                return False
            
            # all tests passed, so we have found a root-matched embedding.
            # all children of superN in this case MUST be unused (subN is a leaf)
            nodemap = {subN:superN}
            self._record_and_propagate(superN, subN, nodemap)
            
            #             self.T[superN][subN] = nodemap
            #             # propagate to parents:
            #             p = superN.parent
            #             while p is not None:
            #                 self.T[p][subN] = nodemap
            #                 p = p.parent
            
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
            #if type(self.T[superN][subN]) == dict:
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
            
            # functionality and end-effector check:
            if not self.node_subsumes(superN, subN):
                return False
            
            # check child matching using brute force enumeration:
            if len(superN.children)<len(subN.children):
                # if superN has fewer children than subN, vertex-disjoint embedding is impossible.
                self.T[superN][subN] = False
                return False
            #brute force search for matching:
            for sub_children_perm in permutations(subN.children):
                for super_children_perm in permutations(superN.children, len(subN.children)):
                    merged_nodemap = self._find_valid_matching(super_children_perm, sub_children_perm)
                    if merged_nodemap:
                        # We have found an embedding. Record it and propagate upwards.
                        # add in the parent pairing:
                        merged_nodemap[subN] = superN                        
                        #                         # Merge nodemaps of all child pairings in table:
                        #                         nodemap = []
                        #                         for sup,sub in zip(super_children_perm, sub_children_perm):
                        #                             child_nodemap = self.T[sup][sub]
                        #                             nodemap += child_nodemap.items()
                        #                         nodemap = dict( nodemap )
                        #                         # add in the parent pairing:
                        #                         nodemap[subN] = superN                        
                        #                         self.T[superN][subN] = nodemap
                        
                        #self.T[superN][subN] = (0, superN, merged_nodemap)
                        # record and propagate to parents:
                        self._record_and_propagate(superN, subN, merged_nodemap)
                        
                        #                         p = superN.parent
                        #                         while p is not None:
                        #                             self.T[p][subN] = nodemap
                        #                             p = p.parent
                        #                         return True
                        return True
            # children cannot be matched; embedding fails.
            self.T[superN][subN] = False
            return False
    
    def _record_and_propagate(self, superN, subN, nodemap):
        '''
        Propagates an embedding to all parents of the super node.  Embeddings 
        are stored in the table as: (length_to_root, root_of_embedding, nodemap),
        where root_of_embedding is the node within the tree of superN to which
        subN actually maps.
        '''
        super_path_length = 0
        p = superN
        while p is not None:
            if self.T[p][subN] is None or self.T[p][subN] is False:
                # Make a new list if we haven't entered anything here before.
                self.T[p][subN] = []
            # we should never be overwriting a False entry.
            #assert self.T[p][subN] is not False, 'Attempted to record valid embedding in previously invalidated table spot'
            
            self.T[p][subN].append( (super_path_length, superN, nodemap) )
            if p.parent is not None:
                super_path_length += p.parent_edge.length
            p = p.parent
    
    def _find_valid_matching(self, super_children_order, sub_children_order):
        '''
        Finds a valid matching (if there is one) and returns a merged nodemap.
        Returns False if there is no valid matching.
        ''' 
        # this is for non-length case:
        #return all( type(self.T[sup][sub])==dict for sup,sub in zip(super_children_order, sub_children_order) )
        
        # NOTE: all() evaluates to True if arg is not False or None.
        # NOTE: all( [] ) evaluates to True.
        
        if not all( type(self.T[sup][sub])==list for sup,sub in zip(super_children_order, sub_children_order) ):
            # This ensures topological embedding.
            return False
        # now check lengths:
        # Merge nodemaps of all child pairings in table:
        merged_nodemap = []
        for i, sub_child in enumerate(sub_children_order):
            sub_length = sub_child.parent_edge.length
            super_child = super_children_order[i]
            super_length = super_child.parent_edge.length
            for super_descendent_mapping in self.T[super_child][sub_child]:
                length = super_descendent_mapping[0]
                #root = super_descendent_mapping[1]
                nodemap = super_descendent_mapping[2]
                if super_length + length == sub_length * self.length_scaling:
                    # match found!
                    merged_nodemap += nodemap.items()            
                    break   # (does not trigger else block)
            else:   # triggers when we get all the way through above for loop.
                return False    # no valid length match found.
        # convert merged_nodemap to dict:    
        merged_nodemap = dict( merged_nodemap )
        return merged_nodemap
        
            
              
    def check_topological_embedding_brute(self):
        '''
        Brute-force combinatoric method to check topological embedding
        '''
        N = len(self.subD.nodes) # number of subdesign nodes
        if len(self.superD.nodes) < N:
            # shortcut - fewer nodes in superdesign
            self.AB_nodemap = None
            return False
        for sub_perm in permutations(self.subD.nodes):
            for super_perm in permutations(self.superD.nodes, N):
                self.AB_nodemap = dict (zip(sub_perm, super_perm))
                if self.check_vertex2vertex():
                    if self.check_edge2path():
                        if self.check_vertex_disjointness():
                            return True
        # no embedding found.
        self.AB_nodemap = None
        return False
        
    def check_vertex2vertex(self):
        ''' 
        Returns True if AB_nodemap satisfies vertex to vertex correspondence with A
        embedding B.
        map is a dict.
        '''
        nodemap = self.AB_nodemap
        superD = self.superD
        subD = self.subD
        # ensure AB_nodemap is valid:
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
            if not self.type_subsumes(nodemap[node].type, node.type):
                return False
            # End effectors must map to end-effectors, and may have no children.
            if node.is_end_effector:
                if not nodemap[node].is_end_effector:
                    return False
                if not nodemap[node].children == []:
                    return False
            # check one-to-oneness:
            if nodemap[node] in used_nodes:
                return False
            used_nodes.append(nodemap[node])
        return True
    
    def check_edge2path(self):
        '''
        Returns True if AB_nodemap satisfies edge-to-path correspondence with A
        embedding B.  Length correspondence is checked.
        '''
        #A = embedding.A
        subD = self.subD
        nodemap = self.AB_nodemap
        for edge in subD.edges:
            assert nodemap.has_key(edge.parent), 'Edge parent maps to no node in superdesign'
            super_parent = nodemap[edge.parent]
            assert nodemap.has_key(edge.child), 'Edge child maps to no node in superdesign'
            # find a path that connects super_child to super_parent. Add up all
            # edge lengths along that path.
            super_child = nodemap[edge.child]
            super_path_length = 0
            
            p = super_child
            while p is not super_parent:
                if p.parent is None:
                    return False    # design root reached
                super_path_length += p.parent_edge.length
                p = p.parent   
            #             p = super_child.parent
            #             while p is not super_parent:
            #                 if p is None:
            #                     return False    # root reached
            #                 super_path_length += p.parent_edge.length
            #                 p = p.parent
            # length check:
            if not super_path_length == (edge.length * self.length_scaling):
                return False
        return True
            
    def check_vertex_disjointness(self):
        '''
        Returns True if AB_nodemap is path-vertex disjoint, false otherwise.
        '''
        subD = self.subD
        nodemap = self.AB_nodemap
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