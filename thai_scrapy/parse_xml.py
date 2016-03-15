# -*- coding:utf-8 -*-

import time
import codecs
import os
from lxml import etree

__author__ = 'Gree-gorey'


def texts(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = path + filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                tree = etree.parse(f)
            links = tree.xpath('//link')
            yield links


def main():
    t1 = time.time()

    for link in texts(u'./dailynews.co.th/'):
        for l in link:
            print l.text

    t2 = time.time()
    print t2 - t1


if __name__ == '__main__':
    main()
