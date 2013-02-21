#!/usr/bin/env python
# _*_ coding: utf-8 _*_

"""
simple twitter parser
"""
import re

class Tokenise:
    """
    split the tweet up. idea is to generate a list of words in order.
    extensions could include additional information like punctuation
    """
    EP = r"""['"“”‘’<>«»{}(\)[\]:]"""
    NOT_EP = r"""[a-zA-Z0-9]""" 
    SM_LEFT = r"""([:=]|[;])(|o|O|-)([pP]|[doO]|[D\)\]]|[\(\[])"""
    SM_RIGHT = r"""([pP]|[doO]|[\)\]]|[\(\[])(|o|O|-)([:=]|[;])"""
    
    
    EP_LEFT_RE = re.compile(r"""(\s|^)(%s+)(%s)""" % (EP, NOT_EP))
    EP_RIGHT_RE = re.compile(r"""(%s)(%s+)(\s|$)""" % (NOT_EP, EP))
    WS_RE = re.compile(r'\s+')
    PROTECT_RE = re.compile('('+SM_LEFT+'|'+SM_RIGHT+')')
    
    def __init__(self):
        self.words = []
        
        
    def tokenise(self, text):
        """
        main parsing function
        """
        # remove whitespace
        text = self.WS_RE.sub(' ', text)
        # isolate punctuation from words
        text = self.EP_LEFT_RE.sub(r"\1\2 \3", text)
        text = self.EP_RIGHT_RE.sub(r"\1 \2\3", text)
        # protect any reserved sequences
        self.words = []
        pos = 0
        if self.PROTECT_RE.search(text):
            for mi in self.PROTECT_RE.finditer(text):
                self.words.extend(text[pos:mi.start()].split())
                self.words.append(text[mi.start():mi.end()])
                pos = mi.end()
        else:
            self.words = text.split()
        #
        print self.words
        return self.words
        
    def words(self):
        return self.words



if __name__ == '__main__':
    import pymongo
    p = Tokenise()
    connection = pymongo.connection.Connection()
    db = connection.tweets
    ti = 0
    tweets = db['earthquake']
    for ti in tweets.find():
        text = ti['text']
        if ti==10:
            break
        ti += 1
    connection.close()
