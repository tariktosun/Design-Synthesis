'''
Created on Jan 17, 2014

@author: tarik
'''
import unittest


class Test_Kinematics(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_kinematic_edge2path(self):
        '''
        Tests the edge2path condition, with kinematics.
        '''
        pass_set = []
        fail_set = []
        
        for i, embedding in enumerate(pass_set):
            assert embedding.check_edge2path(), 'Pass set ' + str(i)
            
        for i, embedding in enumerate(fail_set):
            assert not embedding.check_edge2path(), 'Fail set ' + str(i)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()