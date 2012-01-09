# For a slightly less "guess-proof" implmentation - scramble the alphabet
import string

class Shortly:

    def __init__(self):
        self.numerals = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

        # urls to ids
        self.next_id = 1000
        
        # Mock a keyval store accesible by url or by tag
        self.urls = {} # tag => url
        self.tags = {} # url => tag

    def baseN(self, num):
        """ Convert base 10 to base 62 """
        return ((num == 0) and  "0" ) or ( self.baseN(num // 62).lstrip("0") + self.numerals[num % 62])
    

    def rebase(self, word):
        """ Convert from base62 back to base10"""
        chars = list(word)
        pow = len(chars)-1
        sum = 0
        for c in chars:
            pos = self.numerals.find(c)
            sum += pos * 62 ** pow
            pow -= 1
        return sum
    

    def shorten(self, url):
        """ Check list, if new url, insert and bump id
            return "shortened" url
        """ 
        tag = self.tags.get(url, None)

        if tag == None:
            self.next_id += 1
            tag = self.baseN(self.next_id)
            # setup 2-way lookup
            self.urls[tag] = url
            self.tags[url] = tag

        return "http://short.ly/%s" % tag

    def lengthen(self, tag):
        url = self.urls.get(tag,'404')
        return url
        

    def serve(self, url):
        tag = string.replace(url, 'http://short.ly/', '')
        return self.lengthen(tag)


# Test implementation    
s = Shortly()
items = ('http://www.yahoo.com', 'http://www.google.com', 'http://slashdot.org')
for item in items:
    short = s.shorten(item)
    long  = s.serve(short)
    print "%s shortened to %s and served as %s" % (item, short, long)
