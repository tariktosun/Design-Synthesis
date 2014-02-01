'''
Created on Jan 15, 2014

@author: tariktosun
'''
from Embedding.SmoresModule import SmoresModule
from Embedding.SmoresDesign import SmoresDesign


def setUpKinematicGrasperWalker(test_object):
    '''
    Sets up fixtures for the grasper and walker designs in the test class given n 
    as arg.
    '''
    ''' Grasper design: '''
    g_modules = [SmoresModule('0', 0, [4]),
                 SmoresModule('1', 4, [2,3,0]),
                 SmoresModule('2', 4, [2,3]),
                 ]
    # Modules now alternate odd/even on the left / right sides of the tree.
    
    g_modules[0].add_child_module( 2, g_modules[1])
    g_modules[0].add_child_module( 3, g_modules[2])
    
    grasper = SmoresDesign( g_modules[0], g_modules)
    test_object.small_grasper = grasper
    
    ''' Walker Design '''
    w_modules = [SmoresModule('0', 2, []),
                 SmoresModule('1', 2, []),
                 SmoresModule('2', 0, []),
                 SmoresModule('3', 4, []),
                 ]
    
    w_modules[0].add_child_module( 3, w_modules[1])
    w_modules[1].add_child_module( 4, w_modules[2])
    w_modules[1].add_child_module( 0, w_modules[3])
    
    walker = SmoresDesign( w_modules[0], w_modules)
    test_object.small_walker = walker
    
    test_object.WG_small_nodemap = {g_modules[0].nodes[0]: w_modules[0].nodes[3],
                              g_modules[0].nodes[1]: w_modules[1].nodes[1],
                              g_modules[0].nodes[2]: w_modules[2].nodes[1],
                              g_modules[0].nodes[3]: w_modules[1].nodes[0],
                              g_modules[1].nodes[1]: w_modules[2].nodes[4],
                              g_modules[2].nodes[1]: w_modules[3].nodes[1],
                              g_modules[2].nodes[0]: w_modules[3].nodes[0],
                              }
    
    ####### full size walker/grasper below:
    g_full = [SmoresModule('0', 0, [4]),
             SmoresModule('1', 4, [2,3]),
             SmoresModule('2', 4, [2,3]),
             SmoresModule('3', 4, [2,3]),
             SmoresModule('4', 4, [2,3]),
             SmoresModule('5', 4, [2,3,0]),
             SmoresModule('6', 4, [2,3,0]),
             ]
    
    g_full[0].add_child_module( 2, g_full[1] )
    g_full[0].add_child_module( 3, g_full[2])
    g_full[1].add_child_module( 0, g_full[3])
    g_full[3].add_child_module( 0, g_full[5])
    g_full[2].add_child_module( 0, g_full[4])
    g_full[4].add_child_module( 0, g_full[6])
    
    full_grasper = SmoresDesign( g_full[0], g_full)
    test_object.grasper = full_grasper
    
    ''' Walker Design '''
    w_full = [SmoresModule('0', 2, []),
                 SmoresModule('1', 2, []),
                 SmoresModule('2', 0, []),
                 SmoresModule('3', 4, []),
                 SmoresModule('4', 0, []),
                 SmoresModule('5', 4, []),
                 SmoresModule('6', 0, []),
                 SmoresModule('7', 4, []),
                 #
                 SmoresModule('8', 0, []),
                 SmoresModule('9', 4, []),
                 SmoresModule('10', 0, []),
                 SmoresModule('11', 4, []),
                 SmoresModule('12', 0, []),
                 SmoresModule('13', 4, []),
                 ]
    
    w_full[0].add_child_module( 3, w_full[1])
    w_full[1].add_child_module( 4, w_full[2])
    w_full[1].add_child_module( 0, w_full[3])
    w_full[2].add_child_module( 4, w_full[4])
    w_full[3].add_child_module( 0, w_full[5])
    w_full[4].add_child_module( 4, w_full[6])
    w_full[5].add_child_module( 0, w_full[7])
    #
    w_full[0].add_child_module( 4, w_full[8])
    w_full[0].add_child_module( 0, w_full[9])
    w_full[9].add_child_module( 0, w_full[11])
    w_full[11].add_child_module( 0, w_full[13])
    w_full[8].add_child_module( 4, w_full[10])
    w_full[10].add_child_module( 4, w_full[12])
    
    full_walker = SmoresDesign( w_full[0], w_full)
    test_object.walker = full_walker
    
    test_object.WG_nodemap = {g_full[0].nodes[0]: w_full[0].nodes[3],
                              g_full[0].nodes[1]: w_full[1].nodes[1],
                              g_full[0].nodes[2]: w_full[2].nodes[1],
                              g_full[0].nodes[3]: w_full[1].nodes[0],
                              g_full[1].nodes[1]: w_full[2].nodes[4],
                              g_full[2].nodes[1]: w_full[3].nodes[1],
                              g_full[2].nodes[0]: w_full[3].nodes[0],
                              #
                              g_full[4].nodes[1]: w_full[5].nodes[1],
                              g_full[4].nodes[0]: w_full[5].nodes[0],
                              g_full[6].nodes[1]: w_full[7].nodes[1],
                              #
                              g_full[1].nodes[0]: w_full[4].nodes[1],
                              g_full[3].nodes[1]: w_full[4].nodes[4],
                              g_full[3].nodes[0]: w_full[6].nodes[1],
                              g_full[5].nodes[1]: w_full[6].nodes[4],
                              }
    
    
    
    
    
    