# -*- coding:utf-8 -*-

import codecs, os, lxml.etree, logging, json


def trainingset():
    arr = [[]]
    for root2, dirs, files in os.walk('thaipoem.com'):
        for file in files:
            f = codecs.open(os.path.join(root2, file), "r", "utf-8")
            exemel = f.read()
            f.close()
            root = lxml.etree.fromstring(exemel)[1]
            words = root.xpath('./w')
            n = 0
            while n < len(words):
                try:
                    lex = words[n].xpath('./ana')[0]
                    if lex.get('lex') != '' and lex.get('pos') != '':
                        arr[-1].append((lex.get('lex'), lex.get('pos')))
                    else:
                        arr.append([])
                    n += 1
                except:
                    n += 1
            arr.append([])
    final_arr = []
    for x in arr:
        if len(x) > 1:
            final_arr.append(x)
    print 'readdict finished'
    return final_arr


def trainer():
    from nltk.tag import hmm

trainer()
