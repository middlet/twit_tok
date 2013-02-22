#!/usr/bin/env python

"""
tests for the parser
"""

import json
import unittest
from tokenise import Tokenise

class TestTokenise(unittest.TestCase):
    
    def setUp(self):
        self.tok = Tokenise()


def test_generator(a,b):
    def test(self):
        self.assertEqual(self.tok.tokenise(a), b)
    return test
    
def create_tests(fname):
    nfname = fname.split('.')[0]
    lineno = 1
    for line in open('./examples/%s' % fname, 'r'):
        if line: 
            try:
                j = json.loads(line)
                test_name = 'test_%s_%d' % (nfname, lineno)
                test = test_generator(j['t'], j['r']) 
                setattr(TestTokenise, test_name, test)
            except: # error in json
                print 'error : ', line
            lineno += 1


if __name__ == '__main__':
    # generate tests directly from file
    files = ['urls.tweets']
    for fi in files:
        create_tests(fi)
    # run tests
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestTokenise)
    #unittest.TextTestRunner(verbosity=2).run(suite)
