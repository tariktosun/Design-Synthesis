'''
Created on Jan 15, 2014

@author: tariktosun
'''
from Embedding.SmoresModule import SmoresModule
from Embedding.SmoresDesign import SmoresDesign
import copy


def setUpGrasperWalker(test_object):
    '''
    Sets up fixtures for the grasper and walker designs in the test class given n 
    as arg.
    '''
    ''' Grasper design: '''
    g_modules = [SmoresModule('1', 0, []),
                 SmoresModule('2', 1, [3,2]),
                 SmoresModule('3', 1, [3,2]),
                 SmoresModule('3', 1, [3,0,2]),
                 SmoresModule('5', 1, [3,2]),
                 SmoresModule('6', 1, [3,2]),
                 SmoresModule('7', 1, [3,0,2]),
                ]
    g_small = copy.deepcopy( g_modules )
    g_smaller = copy.deepcopy( g_modules )
    # The -1's here are to make the code more readable when compared with the
    # original drawings of the designs I made (where modules numbers start at 1
    # rather than 0)
    g_modules[1-1].add_child_module( 2, g_modules[5-1] )
    g_modules[1-1].add_child_module( 3, g_modules[2-1] )
    g_modules[2-1].add_child_module( 0, g_modules[3-1] )
    g_modules[3-1].add_child_module( 0, g_modules[4-1] )
    g_modules[5-1].add_child_module( 0, g_modules[6-1] )
    g_modules[6-1].add_child_module( 0, g_modules[7-1] )
    grasper = SmoresDesign( g_modules[1-1], g_modules )
    test_object.grasper = grasper
    
    # now make a smaller version:
    g_small[1-1].add_child_module( 2, g_small[5-1] )
    #g_small[1-1].add_child_module( 3, g_small[2-1] )
    g_small[5-1].nodes[0].active = False    #need to hack this for it to work.
    #grasper_small = SmoresDesign( g_small[1-1], [g_small[1-1], g_small[2-1], g_small[5-1]])
    grasper_small = SmoresDesign( g_small[1-1], [g_small[1-1], g_small[5-1]])
    test_object.grasper_small = grasper_small
    
    # ...and an even smaller version:
    grasper_smaller = SmoresDesign( g_smaller[1-1], [g_smaller[1-1]] )
    test_object.grasper_smaller = grasper_smaller
    
    ''' Walker design: '''
    w_modules = [SmoresModule('1', 1, [2,3,0] ),
                 SmoresModule('2', 1, [2,3] ),
                 SmoresModule('3', 1, [2,3] ),
                 
                 SmoresModule('4', 3, [2] ),
                 
                 SmoresModule('5', 0, [2,3] ),
                 SmoresModule('6', 0, [2,3] ),
                 SmoresModule('7', 0, [2,3] ),
                 
                 SmoresModule('8', 0, [2,3] ),
                 SmoresModule('9', 0, [2,3] ),
                 SmoresModule('10', 0, [2,3] ),
                 
                 SmoresModule('11', 2, [3] ),
                 
                 SmoresModule('12', 1, [2,3] ),
                 SmoresModule('13', 1, [2,3] ),
                 SmoresModule('14', 1, [2,3,0] ),
                 ]
    
    w_small = copy.deepcopy( w_modules )
    w_smaller = copy.deepcopy( w_modules )
    
    # First I am connecting the bottom legs (which will be the grasper)
    # right leg:
    w_modules[11-1].add_child_module( 0, w_modules[12-1] )
    w_modules[12-1].add_child_module( 0, w_modules[13-1] )
    w_modules[13-1].add_child_module( 0, w_modules[14-1] )
    # left leg:
    w_modules[11-1].add_child_module( 1, w_modules[10-1] )
    w_modules[10-1].add_child_module( 1, w_modules[9-1] )
    w_modules[9-1].add_child_module( 1, w_modules[8-1] )
    # now for the top two legs:
    #right leg:
    w_modules[11-1].add_child_module( 3, w_modules[4-1] )
    # Note that above is allowed because 11 is the root module.
    w_modules[4-1].add_child_module( 0, w_modules[3-1] )
    w_modules[3-1].add_child_module( 0, w_modules[2-1] )
    w_modules[2-1].add_child_module( 0, w_modules[1-1] )
    # left leg:
    w_modules[4-1].add_child_module( 1, w_modules[5-1] )
    w_modules[5-1].add_child_module( 1, w_modules[6-1] )
    w_modules[6-1].add_child_module( 1, w_modules[7-1] )
    # Node 11 is the root.
    walker = SmoresDesign( w_modules[11-1], w_modules ) 
    test_object.walker= walker
    
    # now make a small version:
    w_small[11-1].add_child_module( 0, w_small[12-1] )
    w_small[11-1].add_child_module( 1, w_small[10-1] )
    walker_small = SmoresDesign( w_small[11-1], [w_small[11-1], w_small[12-1], w_small[10-1]])
    test_object.walker_small = walker_small
    
    # ... and an even smaller version:
    w_smaller[11-1].add_child_module( 1, w_smaller[10-1] )
    walker_smaller = SmoresDesign( w_smaller[11-1], [ w_smaller[11-1], w_smaller[10-1] ])
    test_object.walker_smaller = walker_smaller
    
    
    
    
    
    