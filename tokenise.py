#!/usr/bin/env python

"""
simple twitter parser
"""
import re

class Tokenise:
    """
    split the tweet up. idea is to generate a list of words in order.
    extensions could include additional information like punctuation
    """
    
    def __init__(self):
        self.words = []
        self.ws_re = re.compile(r'\s+')
        
        
    def tokenise(self, text):
        """
        main parsing function
        """
        self.words = []
        # remove whitespace
        text = self.ws_re.sub(' ', text)
        self.words = text.split()
        #
        return self.words
        
    def words(self):
        return self.words



if __name__ == '__main__':
    #import pymongo
    #p = Tokenise()
    #connection = pymongo.connection.Connection()
    #db = connection.tweets
    #tweets = db['earthquake']
    #for ti in tweets.find():
    #    text = ti['text']
    #    nuc = len([bi for bi in text if ord(bi)<=255])
    #    nas = len([bi for bi in text])
    #    if nuc>nas-5:
    #        print text, p.tokenise(text)
    #connection.close()
    def regex_or(*items):
        r = '|'.join(items)
        r = '(' + r + ')'
        return r
    def pos_lookahead(r):
        return '(?=' + r + ')'
    def neg_lookahead(r):
        return '(?!' + r + ')'
    def optional(r):
        return '(%s)?' % r
    
    PunctChars = r'''['".?!,:;]'''
    Entity = '&(amp|lt|gt|quot);'
    UrlStart1 = regex_or('https?://', r'www\.')
    CommonTLDs = regex_or('com','co\\.uk','org','net','info','ca')
    UrlStart2 = r'[a-z0-9\.-]+?' + r'\.' + CommonTLDs + pos_lookahead(r'[/ \W\b]')
    UrlBody = r'[^ \t\r\n<>]*?'  # * not + for case of:  "go to bla.com." -- don't want period
    UrlExtraCrapBeforeEnd = '%s+?' % regex_or(PunctChars, Entity)
    UrlEnd = regex_or( r'\.\.+', r'[<>]', r'\s', '$')
    Url = (r'\b' + 
        regex_or(UrlStart1, UrlStart2) + 
        UrlBody + 
        pos_lookahead( optional(UrlExtraCrapBeforeEnd) + UrlEnd))
    print '(%s)'% Url
    
