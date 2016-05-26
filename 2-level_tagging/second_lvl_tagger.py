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

def re_tag (path, sources):
    tree, fname = read_xml(path)
    sentences = tree.xpath(u"//se")
    for sent in sentences:
        words = sent.xpath(u"//w")
        for word in words:
            anas = word.xpath(u"//ana")
            for ana in anas:
                print ana.get("lex")
                #ana.set(название, значение)
re_tag("c:\\test\\", rules_path)
