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
            yield tree, open_name


def count(tree, open_name):
    text = tree.xpath(u'//text')
    if text:
        try:
            tokens = pythai.word_count(text[0].text)
            return u'success', tokens
        except:
            return u'encoding error', 0
    else:
        return u'parsing error', 0


def write_result(result, encoding_error, parsing_error):
    open_name = u'./result.txt'
    string = u'tokens: ' + str(result) + u'\nencoding error: ' + str(encoding_error) + u'\nparsing error: '\
             + str(parsing_error)
    with codecs.open(open_name, u'w', u'utf-8') as w:
        w.write(string)


def main():
    t1 = time.time()

    result = 0
    encoding_error = 0
    parsing_error = 0

    for xml_tree, open_name in read_xml(u'./texts/'):
        mode, number = count(xml_tree, open_name)
        if mode == u'success':
            result += number
        elif mode == u'encoding error':
            encoding_error += 1
        else:
            parsing_error += 1

    write_result(result, encoding_error, parsing_error)

    t2 = time.time()
    print t2 - t1


if __name__ == '__main__':
    main()
