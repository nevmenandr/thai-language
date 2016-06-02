# -*- coding: utf-8 -*-

import codecs, os, shutil, re
from lxml import etree
rules_path = ""

def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = path + filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                tree = etree.parse(f)
            yield tree, filename
            #return tree, filename


def re_tag (path, sources):
    tree, fname = read_xml(path)
    sentences = tree.xpath(u"//se")
    for sent in sentences:
        words = sent.xpath(u"//w")
        for word in words:
            anas = word.xpath(u"//ana")
            for ana in anas:
                #print ana.get("lex")
                ana.set("test", "AAAA")
#re_tag("c:\\test\\", rules_path)


def walk_t_tag (path, sources):
    for tree, fname in read_xml(path):
        sent = []
        sentences = tree.xpath(u"//se")
        for sent in sentences:
            words = sent.xpath(u"//w")
            #print type(words)
            tag_it(words)
            #for i in xrange(len(words)):
                #anas = words[i].xpath(u"//ana")
                #for ana in anas:
                    #ana.get("lex")
                    #ana.set(название, значение)

def tag_it (words, sources=""):
    for i in xrange(len(words)):
        anas = words[i].xpath(u"//ana")
        for ana in anas:
            if ana.get("lex") in sources:
                pass
            #print ana.get("lex")
walk_t_tag("c:\\test\\", rules_path)
