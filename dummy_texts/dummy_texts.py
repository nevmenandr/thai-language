# -*- coding: utf-8 -*-

'''python
import pythai

pythai.split(u"การที่ได้ต้องแสดงว่างานดี")
»> u"การ ที่ ได้ ต้อง แสดง ว่า งาน ดี"

pythai.word_count(u"การที่ได้ต้องแสดงว่างานดี")
»> 8

pythai.contains_thai(u"hello")
»> False

pythai.contains_thai(u"helloการที่ไ")
»> True
'''


import os
import time
import codecs
import pythai
from lxml import etree

__author__ = 'gree-gorey'


def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = path + filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                tree = etree.parse(f)
            yield tree, filename


def token_iterator(tree):
    text = tree.xpath('//text')[0].text
    tokens = pythai.split(text)
    for token in tokens:
        yield token


def write_xml(tree, path, filename):
    for token in token_iterator(tree):
        print token
    open_name = path + filename
    with codecs.open(open_name, u'w', u'utf-8') as w:
        w.write(u'foo')


def main():
    t1 = time.time()

    for xml_tree, filename in read_xml(u'./corpus_from/'):
        write_xml(xml_tree, u'./corpus_into/', filename)

    t2 = time.time()
    print t2 - t1


if __name__ == '__main__':
    main()