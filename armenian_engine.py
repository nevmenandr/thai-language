# -*- coding:utf-8 -*-

import time
import codecs
import os
from lxml import etree

__author__ = 'gree-gorey'


class PrsItem:
    def __init__(self):
        self.head = u'#sentno\t#wordno\t#lang\t#graph\t#word\t#indexword\t#nvars\t#nlems\t#nvar\t#lem\t#trans\t' \
                    u'#trans_ru\t#lex\t#gram\t#flex\t#punctl\t#punctr\t#sent_pos\n'
        self.docid = None
        self.author = None
        self.title = None
        self.date1 = None
        self.date2 = None
        self.genre = None
        self.words = None
        self.sentences = None
        self.date_displayed = None
        self.data = None

    def get_text(self):
        result = self.head + self.sentences
        return result


def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = path + filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                tree = etree.parse(f)
            yield tree


def write_prs(tree, text_id, path):
    new_prs = PrsItem()
    sentences = tree.xpath('//body/se')
    new_prs.sentences = u'#meta.sentences\t' + str(len(sentences)) + u'\n'
    for i, sentence in enumerate(sentences):
        pass
        # print i, sentence

    prs_result = new_prs.get_text()
    write_name = path + u'text_id_' + str(text_id) + u'.prs'
    with codecs.open(write_name, u'w', u'utf-8') as w:
        w.write(prs_result)


def main():
    t1 = time.time()

    text_id = 0

    for xml_tree in read_xml(u'./corpus_from/'):
        text_id += 1
        write_prs(xml_tree, text_id, u'./corpus_into/')

    t2 = time.time()
    print t2 - t1


if __name__ == '__main__':
    main()
