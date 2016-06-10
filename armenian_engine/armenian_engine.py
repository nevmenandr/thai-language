# -*- coding:utf-8 -*-

import os
import time
import json
import codecs
import commands
from lxml import etree

__author__ = 'gree-gorey'


class PrsItem:
    def __init__(self):
        self.docid = None
        self.title = u''
        self.genre = u''
        self.words = 0
        self.sentences = 0
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
        self.translit = None
        self.pos = None
        self.punct = ''
        self.sent = ''

    def get_result(self):
        pos = self.pos.split(',')
        return (str(self.sentence_number) + '\t' + str(self.word_number) + '\t\t\t' + self.content + '\t\t' +
                str(self.nvar) + '\t' + str(self.nlems) + '\t' + str(self.self_number) + '\t' + self.lemma + '\t' +
                self.translation + '\t\t' + pos[0] + '\t' + ' '.join(pos[1::]) + '\t\t\t' + self.punct + '\t' +
                self.sent).replace('\r\n', '').replace('\n', '') + '\n'


def load_index():
    return json.load(codecs.open('index.json', 'r', 'utf-8'))['index']


def dump_index(index):
    w = codecs.open('index.json', 'w', 'utf-8')
    json.dump({'index': index}, w, ensure_ascii=False, indent=2)
    w.close()


def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = os.path.join(root, filename)
            with codecs.open(open_name, 'r', 'utf-8') as f:
                tree = None
                try:
                    tree = etree.parse(f)
                except:
                    continue
                if tree:
                    yield tree, open_name


def create_empty_folder_tree(open_root, write_root):
    for root, dirs, files in os.walk(open_root):
        for directory in dirs:
            path_to_dir = os.path.join(root, directory).replace(open_root, write_root)
            if not os.path.exists(path_to_dir):
                os.makedirs(path_to_dir)


def write_prs(tree, write_name, index):
    prs = PrsItem()
    prs.docid = index
    prs.title = tree.xpath('//meta/title')[0].text
    prs.genre = tree.xpath('//meta/genre')[0].text
    sentences = tree.xpath('//body/se')
    prs.sentences = len(sentences)
    for i, sentence in enumerate(sentences, start=1):
        words = sentence.xpath('./w')
        prs.words = len(words)
        for j, word in enumerate(words, start=1):
            content = u''.join([x for x in word.itertext()])
            content = content.replace(u' ', u'')
            content = content.replace(u' ', u'')
            content = content.replace(u'\t', u'')
            content = content.replace(u'\r\n', u'')
            content = content.replace(u'\n', u'')
            if not content:
                continue
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
                new_word.lemma = analysis.get('lex')
                new_word.pos = analysis.get('pos')
                new_word.translation = analysis.get('trans')
                new_word.translit = analysis.get('translit')
                if j == len(words):
                    new_word.sent = 'eos'
                    new_word.punct = u' '
                if j == 1:
                    new_word.sent = 'bos'

                word_result = new_word.get_result()
                prs.data.append(word_result)

    prs_result = prs.get_text()
    with codecs.open(write_name, 'w', 'utf-8') as w:
        w.write(prs_result)


def main():
    t1 = time.time()

    files = int(commands.getstatusoutput('find ./texts_tagged/ -type f | wc -l')[1])

    # files = 1000

    print 'Total number of files: ' + str(files)
    print

    index = load_index()

    open_root = './texts_tagged/'
    # write_root = './texts_tagged_armenian/'
    write_root = '/var/www/web-corpora.net/ThaiCorpus/languages/thai/parsed_data/'

    create_empty_folder_tree(open_root, write_root)

    i = 0

    for xml_tree, open_name in read_xml(open_root):
        i += 1
        index += 1
        write_name = open_name.replace(open_root, write_root).replace('.xml', '.prs')
        write_prs(xml_tree, write_name, index)

        print round(float(i)/files*100, 3), "% complete...         \r",

    dump_index(index)

    print ''
    print 'FINISHED'

    t2 = time.time()
    print t2 - t1


if __name__ == '__main__':
    main()
