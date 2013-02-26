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
    EP = r"""['"“”‘’«»{}(\)[\]]"""
    NOT_EP = r"""[a-zA-Z0-9]""" 
    PC = r"""['"“”‘’.?!…,:;]"""
    ENT = r"""&(?:amp|lt|gt|quot);"""
    SM_LEFT = r"""([:=]|[;])(|o|O|-)([pP]|[doO]|[D\)\]]|[\(\[])"""
    SM_RIGHT = r"""([pP]|[doO]|[\)\]]|[\(\[])(|o|O|-)([:=]|[;])"""
    URLS = r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))"""    
    EMAIL = r"""\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.\-_]+[A-Za-z]{2,4}\b"""
    TIME = r"""\d+(?::\d+){1,2}"""
    NUMS = r"""[\$€£¥]?\d+(?:[,.]\d*)*%?"""
    PUNC = r"""['"“”‘’]+|[.?!,…]+|[:;]+"""
    APOSWORD = r"""[^\s.,?"]+['’′][^\s.,?"]*"""
    HEARTS = r"""(?:<+/?3+)+"""
    ARROWS = r"""(?:<*[-―—=]*>+|<+[-―—=]*>*)"""
    ABBREV = "([A-Za-z](\.[A-Za-z])+\.?)"
    
    REGEX = '('+HEARTS+'|'+URLS+'|'+EMAIL+'|'+TIME+'|'+NUMS+'|'+ \
        SM_RIGHT+'|'+SM_LEFT+'|'+ARROWS+'|'+ENT+'|'+PUNC+'|'+ \
        ABBREV + ')'
    
    EP_LEFT_RE = re.compile(r"""(\s|^)(%s+)(%s)""" % (EP, NOT_EP))
    EP_RIGHT_RE = re.compile(r"""(%s)(%s+)(\s|$)""" % (NOT_EP, EP))
    WS_RE = re.compile(r'\s+')
    PROTECT_RE = re.compile(REGEX)
    
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
            self.words.extend(text[pos:len(text)].split())
        else:
            self.words = text.split()
        #
        #print self.words
        return self.words
        
    def words(self):
        return self.words



if __name__ == '__main__':
    import pymongo
    p = Tokenise()
    connection = pymongo.connection.Connection()
    db = connection.tweets
    tind = 0
    tweets = db['flood']
    for ti in tweets.find():
        #text = ti['text']
        urls = ti['entities']['urls']
        if urls:
            for ui in urls:
                print (u''+ui['url']).encode('utf-8')
        #if tind==10:
        #    break
        tind += 1
    connection.close()
