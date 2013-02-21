#!/usr/bin/env python

"""
tests for the parser
"""

import unittest
from parser import Parse

class TestParser(unittest.TestCase):
    
    def setUp(self):
        self.parse = Parse()
    
    def test_simple(self):
        """
        very easy to parse tweets
        basic handling of the texts. all made up tweets
        """        
        for ti in open('examples/simple.txt', 'r'):
            j = json.loads(ti)
            self.assertEqual(self.parse.parse_tweet(j['t']), j['r'])
        
    



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
    unittest.TextTestRunner(verbosity=2).run(suite)
