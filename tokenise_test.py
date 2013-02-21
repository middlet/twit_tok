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


if __name__ == '__main__':
    # generate tests directly from file
    lineno = 1
    for line in open('./examples/simple.tweets', 'r'):
        j = json.loads(line)
        test_name = 'test_simple_%d'%lineno
        test = test_generator(j['t'], j['r']) 
        setattr(TestTokenise, test_name, test)
        lineno += 1

    suite = unittest.TestLoader().loadTestsFromTestCase(TestTokenise)
    unittest.TextTestRunner(verbosity=2).run(suite)
