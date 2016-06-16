# -*- coding: utf-8 -*-
import codecs
import nltk
import dill
import lxml.etree

with open('my_tagger.dill', 'rb') as f:
    hmm_tagger = dill.load(f)

def predict_untagged(filename):
    f=codecs.open(filename, 'r', 'utf-8')
    text=f.read()
    f.close()
    arr=[]
    result=''
    root = lxml.etree.fromstring(exemel)[1]
    words = root.xpath('./w')
    for i in words:
        arr.append(i.text)
    bp=hmm_tagger.tag(arr)
    print bp

predict_untagged('thaipoem.com\10098.xml')
