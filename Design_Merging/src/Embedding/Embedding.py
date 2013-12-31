'''
Created on Dec 30, 2013

@author: tariktosun
'''

class Embedding(object):
    '''
    Embedding class, specifying the way one design may embed another.
    '''


    def __init__(self, superD, subD, nodemap):
        '''
        Constructor
        '''
        self.superD = superD
        self.subD = subD
        self.nodemap = nodemap