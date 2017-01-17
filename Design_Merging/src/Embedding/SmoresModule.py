'''
Created on Jan 15, 2014

@author: tariktosun
'''

import Node

class SmoresModule(object):
    '''
    Object representing a SMORES robot module for design synthesis project.
    A SMORES module is composed of four nodes, which are numbered as follows:
            0
            |
        2 - 1 - 3
            |
            4
    Edge 0-1, 1-2, and 1-3 are CR, and edge 1-4 is a hinge.  All nodes are type
    2. All nodes are active by default.  The user may specify which nodes are 
    inactive using arguments to the constructor and add_child functions.
    '''


    def __init__(self, name, root_node_number, inactive_nodes_numbers=[]):
        '''
        Constructor.  root_node is a number (0-3) specifying which node in this
        module is the root.  inactive_nodes is a list of numbers (again, 0-3)
        specifying which nodes should be considered inactive in this module.
        '''
        # name:
        self.name = name
        # root node number:
        self.root_node_number = root_node_number
        # list of child modules:
        self.child_modules = [None, None, None, None, None]    # note that only 3 may be used.
        # parent module:
        self.parent_module = None
        
        # set up list of nodes.  The order is important.
        self.nodes = [Node.Node(self.name+"-"+str(i)) for i in range(5)]
        # set activity:
        for i in inactive_nodes_numbers:
            self.nodes[i].active = False
        # set types:
        for i in xrange(5):
            self.nodes[i].type = 2

        # create structure based on root:
        n = self.nodes # for easy typing...
        if root_node_number == 0:
            n[0].add_child( n[1] )#, 1 )
            n[1].add_child( n[2] )#, 1 )
            n[1].add_child( n[3] )#, 1 )
            n[1].add_child( n[4] )#, 1 )
        if root_node_number == 1:
            assert False, 'Node 1 cannot be the root.'            
            n[1].add_child( n[0] )#, 1 )
            n[1].add_child( n[2] )#, 1 )
            n[1].add_child( n[3] )#, 1 )
            n[1].add_child( n[4] )#, 1 )
        if root_node_number == 2:
            n[2].add_child( n[1] )#, 1 )
            n[1].add_child( n[0] )#, 1 )
            n[1].add_child( n[3] )#, 1 )
            n[1].add_child( n[4] )#, 1 )
        if root_node_number == 3:
            n[3].add_child( n[1] )#, 1 )
            n[1].add_child( n[0] )#, 1 )
            n[1].add_child( n[2] )#, 1 )
            n[1].add_child( n[4] )#, 1 )
        if root_node_number == 4:
            n[4].add_child( n[1] )#, 1 )
            n[1].add_child( n[0] )#, 1 )
            n[1].add_child( n[2] )#, 1 )
            n[1].add_child( n[3] )#, 1 )
            
    def add_child_module(self, node_number, child_module):
        '''
        Adds a child module to this module, connected at specified node number.
        '''
        assert isinstance(child_module, SmoresModule), 'child_module is not a SmoresModule object.'
        if self.parent_module is not None:
            assert node_number is not self.root_node_number, 'Attempted to add child module at root_node_number to non-root module.'
            assert node_number is not 1, 'Cannot add child_module at node 1.'
        assert self.child_modules[node_number] is None, 'Attempted to add a child to a filled node_number.'
        # add to list of children:
        self.child_modules[node_number] = child_module
        child_module.parent_module = self
        # connect root node of child module to specified node of this module:
        # Rather than add a rigid connection, we're going to fuse two nodes
        n = self.nodes[node_number] #node in the parent which will be fused.
        p = n.parent
        assert p is not None, 'Cannot add children to root node of design.'
        r = child_module.nodes[child_module.root_node_number] # root node in the child module (to be fused).
        # fuse names:
        r.name = n.name + '/' + r.name
        # connect n's parent node to r:
        p.children.append(r)
        p.children.remove(n)
        #p.child_frames[r] = p.child_frames[n]
        #del p.child_frames[n]
        r.parent = p
        # handle the edge:
        n.parent_edge.child = r
        r.parent_edge = n.parent_edge
        # handle node list in the module:
        self.nodes[node_number] = r # node n is no longer needed; it has been fused into r.

        # # Edge length depends on the kind of nodes involved:
        # length = 0
        # if node_number == 1:
        #     length +=1
        # if child_module.root_node_number == 1:
        #     length +=1
        # self.nodes[node_number].add_child(child_module.nodes[child_module.root_node_number], length)

        # 
        

        
    def remove_child_module(self, child_module):
        '''
        Removes a child module from this module.
        '''
        assert child_module in self.child_modules, 'child_module was not in this module\'s list of children.'
        assert child_module.parent_module is self, 'This module was not child_module\'s  parent.'
        # remove from list of child modules:
        child_module_number = self.child_modules.index(child_module)
        self.child_modules[child_module_number] = None
        # Break the connection between nodes:
        self.nodes[child_module_number].remove_child(child_module.parent_module)
        
        
        
        
        
        