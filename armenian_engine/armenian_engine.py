# -*- coding:utf-8 -*-

import os
import re
import time
import codecs
from lxml import etree

__author__ = 'gree-gorey'


class PrsItem:
    def __init__(self):
        self.docid = None
        self.title = None
        self.genre = None
        self.words = None
        self.sentences = None
        self.data = []

    def get_text(self):
        head = u'#sentno\t#wordno\t#lang\t#graph\t#word\t#indexword\t#nvars\t#nlems\t#nvar\t#lem\t#trans\t' \
               u'#trans_ru\t#lex\t#gram\t#flex\t#punctl\t#punctr\t#sent_pos\n'
        docid = u'#meta.docid\t' + str(self.docid) + u'\n'
        author = u'#meta.author\t\n'
        title = u'#meta.title\t' + self.title + u'\n'
        date1 = u'#meta.date1\t\n'
        date2 = u'#meta.date2\t\n'
        genre = u'#meta.genre\t' + self.genre + u'\n'
        words = u'#meta.words\t' + str(self.words) + u'\n'
        sentences = u'#meta.sentences\t' + str(self.sentences) + u'\n'
        date_displayed = u'#meta.date_displayed\t\n'
        body = u''.join(self.data)
        result = head + docid + author + title + date1 + date2 + genre + words + sentences + date_displayed + body
        return result


class Word:
    def __init__(self):
        self.content = None
        self.pos = None
        self.sentence_number = None
        self.word_number = None
        self.nvar = None
        self.nlems = None
        self.self_number = None
        self.lemma = None
        self.translation = None
        self.pos = None
        self.sent = u''

    def get_result(self):
        pos = self.pos.split(u',')
        return str(self.sentence_number) + u'\t' + str(self.word_number) + u'\t\t\t' + self.content + u'\t\t' +\
               str(self.nvar) + u'\t' + str(self.nlems) + u'\t' + str(self.self_number) + u'\t' + self.lemma + u'\t\t' +\
               self.translation + u'\t' + pos[0] + u'\t' + u' '.join(pos[1::]) + u'\t\t\t\t' + self.sent + u'\n'


def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = path + filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                tree = etree.parse(f)
            yield tree


def write_prs(tree, text_id, path):
    prs = PrsItem()
    prs.docid = text_id
    prs.title = tree.xpath('//meta/title')[0].text
    prs.genre = tree.xpath('//meta/genre')[0].text
    sentences = tree.xpath('//body/se')
    prs.sentences = len(sentences)
    for i, sentence in enumerate(sentences, start=1):
        words = sentence.xpath('./w')
        for j, word in enumerate(words, start=1):
            content = u''.join([x for x in word.itertext()])
            content = re.sub(u' +', u'', content, re.U)
            content = re.sub(u'\r\n+', u'', content, re.U)
            content = re.sub(u'\n+', u'', content, re.U)
            analyses = word.xpath('./ana')
            nvar = len(analyses)
            lemmata = len(set([analysis.get('lex') for analysis in analyses]))
            for k, analysis in enumerate(analyses, start=1):
                new_word = Word()
                new_word.content = content
                new_word.sentence_number = i
                new_word.word_number = j
                new_word.self_number = k
                new_word.nvar = nvar
                new_word.nlems = lemmata
                new_word.lemma = analysis.get(u'lex')
                new_word.translation = analysis.get(u'trans')
                new_word.pos = analysis.get(u'gr')
                if j == len(words):
                    new_word.sent = u'eos'
                if j == 1:
                    new_word.sent = u'bos'

                word_result = new_word.get_result()
                prs.data.append(word_result)

    prs_result = prs.get_text()
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
