'''
Created on Dec 30, 2013

@author: tariktosun
'''

import Design
from itertools import permutations
import pandas
#import sys
import math

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
        # check validity before returning.
        self.check_validity()
        
    def check_validity(self):
        '''
        Checks the validity of this Embedding. Throws assertion error if it fails,
        runs silently otherwise.
        '''
        self.superD.check_validity()
        self.subD.check_validity()
        # check that types_subsumed is consistent:
        for t in self.types_subsumed.keys():
            subsumed_types = self.types_subsumed[t]
            # Type must subsume itself:
            assert t in subsumed_types, 'Invalid types_subsumed.'
            # any type subsumed must also be in the dict as a key:
            for s in subsumed_types:
                assert self.types_subsumed.has_key(s), 'Invalid types_subsumed'
        # check that designs include only types in the table:
        for n in self.superD.nodes:
            assert self.types_subsumed.has_key(n.type), 'A node has an invalid type.'
        for n in self.subD.nodes:
            assert self.types_subsumed.has_key(n.type), 'A node has an invalid type.'
            
        
        
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
        #T_list = [[self.pretty_nodemap(self.T[superN][subN]) for subN in self.subD.nodes]
        #           for superN in self.superD.nodes]
        T_list = [[0 for _ in range(len(self.subD.nodes))] for _ in range(len(self.superD.nodes))]
        for i,superN in enumerate(self.superD.nodes):
            for j,subN in enumerate(self.subD.nodes):
                if type(self.T[superN][subN]) == list:
                    T_list[i][j] = True
                else:
                    T_list[i][j] = self.T[superN][subN]
                      
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
        # Clear table and nodemap:
        self.T = { superN:{ subN:None for subN in self.subD.nodes } 
                  for superN in self.superD.nodes }  
        self.AB_nodemap = None
        boolean_result = self._embeds(self.superD.root_node, self.subD.root_node)
        if boolean_result:
            # take the first valid embedding stored at the root.
            (_, _, nodemap) = self.T[self.superD.root_node][self.subD.root_node][0]
            self.AB_nodemap = nodemap
        else:
            self.AB_nodemap = False
        return boolean_result
        
    def _embeds(self, superN, subN):
        '''
        Recursive function testing subtree embedding.
        '''
        # This function should not be called more than once for a pairing.
        #assert self.T[superN][subN] is None, 'Attempted to call _embeds on a filled table entry.'
        # not actually true!!!
        
        if superN.children == [] and subN.children == []:
            ''' base case 1: nodes with no children.
            Embeds if:
                subN may map to superN.
            '''
            
            # functionality and end-effector check:
            if not self.node_subsumes(superN, subN):
                self.T[superN][subN] = False
                return False
            
            # We have found an embedding. Record it and propagate upwards:
            nodemap = {subN:superN}
            self._record_and_propagate(superN, subN, nodemap)            
            return True
        elif subN.children == []:
            ''' base case 2: superN has children, but subN does not.
            Embeds if:
                (1) subN may embed in a child of superN
                (2) subN is not an end-effector, and may map to superN
            '''
             
            # Recursively ensure that all pairs of subN with children of superN
            # have table entries:
            self._ensure_rooted_entries(superN, subN)
            
            ''' (2) Does subN map to superN? '''      
            # functionality and end-effector check:
            if not self.node_subsumes(superN, subN):
                ''' (1) Does subN embed in a child of superN? '''
                # We may still have an embedding if an embedding in a child was found (and propagated up)
                #if type(self.T[superN][subN]) == dict:
                if type(self.T[superN][subN]) == list:
                    return True
                else:
                    self.T[superN][subN] = False
                    return False
            
            # all tests passed, so we have found a root-matched embedding.
            # all children of superN in this case MUST be unused (subN is a leaf)
            nodemap = {subN:superN}
            self._record_and_propagate(superN, subN, nodemap)
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
                  
            # Recursively ensure that all pairs of subN with children of superN
            # have table entries:
            self._ensure_rooted_entries(superN, subN)
            #             for superC in superN.children:
            #                 if self.T[superC][subN] == None:
            #                     self._embeds(superC, subN)
            
            ''' (2) Can a matching be found between children of subN and superN,
                    and can subN map to superN? ''' 
            # Recursively ensure that all child pairings have table entries:
            for subC in subN.children:
                self._ensure_rooted_entries(superN, subC)
            
            #             for superC in superN.children:
            #                 for subC in subN.children:
            #                     if self.T[superC][subC] == None:
            #                         #self.T[superC][subC] = self._embeds(superC, subC)
            #                         self._embeds(superC, subC)
            
            # functionality and end-effector check:
            if not self.node_subsumes(superN, subN):
                ''' (1) does subN embed in a child of superN? '''
                # return True if an embedding in a child was found (and propagated up)
                if type(self.T[superN][subN]) == list:
                    return True
                else:
                    self.T[superN][subN] = False
                    return False
            
            # check child matching using brute force enumeration:
            if len(superN.children)<len(subN.children):
                # if superN has fewer children than subN, vertex-disjoint embedding is impossible.
                ''' (1) does subN embed in a child of superN? '''
                # return True if an embedding in a child was found (and propagated up)
                if type(self.T[superN][subN]) == list:
                    return True
                else:
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
                        # record and propagate to parents:
                        self._record_and_propagate(superN, subN, merged_nodemap)
                        return True
            # children cannot be matched; embedding fails.
            ''' (1) does subN embed in a child of superN? '''
            # return True if an embedding in a child was found (and propagated up)
            if type(self.T[superN][subN]) == list:
                return True
            else:
                self.T[superN][subN] = False
                return False
            
    def _ensure_rooted_entries(self, superN, subN):
            '''
            Ensures that a rooted table entry for subN and each of superN's
            children exists in the table.  If an entry does not exist yet, 
            _embeds is called with those nodes in order to create one.
            '''
            for superC in superN.children:
                if self.T[superC][subN] == None:
                    self._embeds(superC, subN)
                elif self.T[superN][subN] == False:
                    continue
                elif type(self.T[superC][subN]) == list:
                    # find an embedding rooted at superC and subN
                    for mapping in self.T[superC][subN]:
                        #length = mapping[0]
                        root = mapping[1]
                        #nodemap = mapping[2]
                        if root == superC:
                            break   # rooted entry found
                    else:   # no rooted embedding found
                        self._embeds(superC, subN)
    
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
            if self.T[p][subN] is None:# or self.T[p][subN] is False:
                # Make a new list if we haven't entered anything here before.
                self.T[p][subN] = []
            # we should never be overwriting a False entry.
            assert self.T[p][subN] is not False, 'Attempted to record valid embedding in previously invalidated table spot'
            
            self.T[p][subN].append( (super_path_length, superN, nodemap) )
            if p.parent is not None:
                super_path_length += p.parent_edge.length
            p = p.parent
            #             if superN.name == '11-3' and subN.name == '1-3':
            #                 pass
        return
    
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
              
    def check_topological_embedding_brute(self, verbose=False):
        '''
        Brute-force combinatoric method to check topological embedding
        '''
        # Clear table and nodemap:
        self.T = { superN:{ subN:None for subN in self.subD.nodes } 
                  for superN in self.superD.nodes }  
        self.AB_nodemap = None
        N = len(self.subD.nodes) # number of subdesign nodes
        if len(self.superD.nodes) < N:
            # shortcut - fewer nodes in superdesign
            self.AB_nodemap = None
            return False
        # compute number of matchings:
        num_matchings = math.factorial(len(self.subD.nodes))*math.factorial(len(self.superD.nodes))
        count = 0
        for sub_perm in permutations(self.subD.nodes):
            for super_perm in permutations(self.superD.nodes, N):
                #sys.stdout.write("%d  \r" % count )
                #sys.stdout.flush()    # carriage returns don't work in Eclipse :-(
                if verbose:
                    print str(count) + " / " + str(num_matchings)
                    count += 1
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