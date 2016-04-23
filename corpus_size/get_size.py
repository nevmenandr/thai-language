# -*- coding: utf-8 -*-

import os
import time
import codecs
import pythai
from lxml import etree

__author__ = 'gree-gorey'


def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = os.path.join(root, filename)
            with codecs.open(open_name, u'r', u'utf-8') as f:
                try:
                    tree = etree.parse(f)
                except:
                    tree = etree.XML(u'<dummy>foo</dummy>')
            yield tree


def count(tree):
    text = tree.xpath('//text')
    if text:
        tokens = pythai.split(text[0].text)
        return len(tokens)
    else:
        return 0


def write_result(result):
    open_name = u'./result.txt'
    with codecs.open(open_name, u'w', u'utf-8') as w:
        w.write(str(result))


def main():
    t1 = time.time()

    result = 0

    for xml_tree in read_xml(u'./texts/'):
        result += count(xml_tree)

    write_result(result)

    t2 = time.time()
    print t2 - t1


if __name__ == '__main__':
    main()
