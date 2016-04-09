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
            open_name = path + filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                tree = etree.parse(f)
            yield tree, filename


def token_iterator(sentence):
    tokens = pythai.split(sentence)
    for token in tokens:
        yield token


def sentence_iterator(tree):
    text = tree.xpath('//text')[0].text
    sentences = text.split(u' ')
    for sentence in sentences:
        yield sentence


def write_xml(tree, path, filename):
    new_document = etree.Element(u'body')
    xml_doc = etree.ElementTree(new_document)
    meta = etree.Element(u'meta')
    link = etree.Element(u'link')
    title = etree.Element(u'title')
    genre = etree.Element(u'genre')
    title.text = u'title'
    genre.text = u'genre'
    meta.append(link)
    meta.append(title)
    meta.append(genre)
    new_document.append(meta)
    for sentence in sentence_iterator(tree):
        se = etree.Element(u'se')
        for token in token_iterator(sentence):
            word = etree.Element(u'w')
            ana = etree.Element(u'ana')
            ana.attrib[u'lex'] = token
            ana.attrib[u'morph'] = u''
            ana.attrib[u'gr'] = u'S,nom,sg'
            ana.attrib[u'trans'] = token
            word.append(ana)
            word.text = token
            se.append(word)
        new_document.append(se)

    open_name = path + filename
    with codecs.open(open_name, u'w') as w:
        xml_doc.write(w, encoding=u'utf-8')


def main():
    t1 = time.time()

    for xml_tree, filename in read_xml(u'./corpus_from/'):
        write_xml(xml_tree, u'./corpus_into/', filename)

    t2 = time.time()
    print t2 - t1


if __name__ == '__main__':
    main()