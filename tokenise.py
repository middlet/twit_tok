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
    PC = r"""['"“”‘’.?!…,:;]"""
    ENT = r"""&(?:amp|lt|gt|quot);"""
    SM_LEFT = r"""([:=]|[;])(|o|O|-)([pP]|[doO]|[D\)\]]|[\(\[])"""
    SM_RIGHT = r"""([pP]|[doO]|[\)\]]|[\(\[])(|o|O|-)([:=]|[;])"""
    #URLS = r"""(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))"""
    URLS1  = r"""(?:https?://|\bwww\.)"""
    CTLD = r"""(?:com|org|edu|gov|net|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|pro|tel|travel|xxx)"""
    CCTLD = r"""(?:ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|ss|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|za|zm|zw)"""
    URLS2 = r"""\b(?:[A-Za-z\d-])+(?:\.[A-Za-z0-9]+){0,3}\.""" + """(?:"""+CTLD+"""|"""+CCTLD+""")"""+"""(?:\."""+CCTLD+""")?(?=\W|$)"""
    URLB = r"""(?:[^\.\s<>][^\s<>]*?)?"""
    URLEC = r"""(?:"""+PC+"""|"""+ENT+""")+?"""
    URLE = r"""(?:\.\.+|[<>]|\s|$)"""
    URLS = r"""(?:"""+URLS1+"""|"""+URLS2+""")"""+URLB+"""(?=(?:"""+URLEC+""")?"""+URLE+""")"""
    
    
    EP_LEFT_RE = re.compile(r"""(\s|^)(%s+)(%s)""" % (EP, NOT_EP))
    EP_RIGHT_RE = re.compile(r"""(%s)(%s+)(\s|$)""" % (NOT_EP, EP))
    WS_RE = re.compile(r'\s+')
    PROTECT_RE = re.compile('('+SM_LEFT+'|'+SM_RIGHT+'|'+URLS+')')
    
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
