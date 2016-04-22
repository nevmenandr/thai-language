# -*- coding: utf-8 -*-

import os
import codecs
from lxml import etree

__author__ = 'gree-gorey'


def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = path + filename
            print filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                tree = etree.parse(f)
            return tree, filename


def main():
    tree, filename = read_xml(u'./corpus_from_tagged/')
    se = tree.xpath('//meta/link')
    print filename
    print se[0].text

if __name__ == '__main__':
    main()
