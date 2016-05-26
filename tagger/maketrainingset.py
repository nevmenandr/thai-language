# -*- coding:utf-8 -*-

import codecs, os, lxml.etree

def trainingset():
    arrwords = []
    for root2, dirs, files in os.walk('thaipoem.com'):
        for file in files:
            f = codecs.open(os.path.join(root2, file), "r", "utf-8")
            exemel = f.read()
            f.close()
            root = lxml.etree.fromstring(exemel)[1]
            #print root.tag
            words = root.xpath('./w')
            for i in words:
                try:
                    lex=i.xpath('/ana')[0]
                    print lex.get('lex')
                except:
                    pass
    print 'readdict finished'
    return arrwords

trainingset()
