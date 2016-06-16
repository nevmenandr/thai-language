# -*- coding: utf-8 -*-

import os
import time
import json
import codecs
# import commands
import pythai
from lxml import etree

__author__ = 'gree-gorey'


def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = os.path.join(root, filename)
            with codecs.open(open_name, u'r', u'utf-8') as f:
                tree = None
                try:
                    tree = etree.parse(f)
                except:
                    continue
                if tree:
                    yield tree, open_name


def iterate_sources(path):
    # собираем все папки разных ресурсов
    sources = []
    for root, dirs, files in os.walk(path):
        for source in dirs:
            sources.append(os.path.join(root, source))

    # обходим все эти папки по очереди
    for source in sources:
        yield source


def create_empty_folder_tree(open_root, write_root):
    for root, dirs, files in os.walk(open_root):
        for directory in dirs:
            path_to_dir = os.path.join(root, directory).replace(open_root, write_root)
            if not os.path.exists(path_to_dir):
                os.makedirs(path_to_dir)


def sentence_iterator(tree):
    # try:
    text = tree.xpath(u'//text')[0].text
    # except:
    #     return False
    sentences = [[u'', True]]
    previous_is_thai = True
    for char in text:
        if not (32 <= ord(char) <= 126 or 3585 <= ord(char) <= 3675):
            continue
        if 3585 <= ord(char) <= 3675:
            if not previous_is_thai:
                sentences.append([u'', True])
            sentences[-1][0] += char
            previous_is_thai = True
        else:
            if previous_is_thai:
                sentences.append([u'', False])
            sentences[-1][0] += char
            previous_is_thai = False
    for sentence, is_thai in sentences:
        if sentence:
            yield sentence, is_thai


def analyze_sentence(sentence, is_thai, dictionary):
    se = etree.Element(u'se')
    if is_thai:
        tokens = pythai.split(sentence)
        for token in tokens:
            if token:
                word = etree.Element(u'w')
                if token in dictionary:
                    for analysis_number in dictionary[token]:
                        analysis = dictionary[token][analysis_number]
                        ana = etree.Element(u'ana')
                        ana.attrib[u'lex'] = token
                        ana.attrib[u'pos'] = u','.join(analysis[1])
                        ana.attrib[u'trans'] = analysis[0]
                        ana.attrib[u'translit'] = analysis[2]
                        word.append(ana)
                word.text = token
                se.append(word)
    else:
        sentence = u' '.join(sentence.split())
        sentence = sentence.replace(u'\t', u'')
        sentence = sentence.replace(u'\r\n', u'')
        sentence = sentence.replace(u'\n', u'')
        if sentence:
            word = etree.Element(u'w')
            ana = etree.Element(u'ana')
            ana.attrib[u'lex'] = u''
            ana.attrib[u'pos'] = u''
            ana.attrib[u'trans'] = u''
            ana.attrib[u'translit'] = u''
            word.append(ana)
            word.text = sentence
            se.append(word)
    return se


def write_xml(tree, dictionary, write_name):
    new_document = etree.Element(u'body')
    xml_doc = etree.ElementTree(new_document)
    meta = etree.Element(u'meta')
    link = etree.Element(u'link')
    title = etree.Element(u'title')
    genre = etree.Element(u'genre')
    if tree.xpath('//link'):
        link.text = tree.xpath('//link')[0].text
    if tree.xpath('//title'):
        text = tree.xpath('//title')[0].text
        text = u' '.join(text.split())
        text = text.replace(u'\t', u'')
        text = text.replace(u'\r\n', u'')
        text = text.replace(u'\n', u'')
        title.text = text
    if tree.xpath('//genre'):
        genre.text = tree.xpath('//genre')[0].text
    meta.append(link)
    meta.append(title)
    meta.append(genre)
    new_document.append(meta)

    tokens = 0

    for sentence, is_thai in sentence_iterator(tree):
        se = analyze_sentence(sentence, is_thai, dictionary)
        if len(se) > 0:
            new_document.append(se)
            tokens += len(se)

    with codecs.open(write_name, u'w') as w:
        xml_doc.write(w, encoding=u'utf-8')

    return tokens


def main():
    t1 = time.time()

    # files = int(commands.getstatusoutput('find . -type f | wc -l')[1])

    # files = 1000

    # print 'Total number of files: ' + str(files)
    # print

    dictionary = json.load(codecs.open(u'./dictionary.json', u'r', u'utf-8'))

    open_root = './texts/'
    write_root = './texts_tagged/'

    create_empty_folder_tree(open_root, write_root)

    i = 0

    total_tokens_number = 0

    residue = 0

    for source in iterate_sources(open_root):

        print 'Begin ' + source + ' folder'

        tokens_in_folder = 0

        limit = 22000000
        number_of_folders = 8
        limit_per_folder = int(float(limit) / number_of_folders)

        if residue != 0:
            limit_per_folder += residue

        print 'Limit for this folder: ' + str(limit_per_folder) + ' tokens'

        for xml_tree, open_name in read_xml(source):
            i += 1

            write_name = open_name.replace(open_root, write_root)

            tokens_here = write_xml(xml_tree, dictionary, write_name)

            tokens_in_folder += tokens_here
            total_tokens_number += tokens_here

            print round(float(total_tokens_number)/limit*100, 3), "% complete...         \r",

            if tokens_in_folder > limit_per_folder:
                break

        if tokens_in_folder < limit_per_folder:
            residue += limit_per_folder - tokens_in_folder
        else:
            residue = 0

        print ''
        print 'In folder ' + source + ': ' + str(tokens_in_folder) + ' tokens'

        # if i > 1000:
        #     break

    print ''
    print 'Total: ' + str(total_tokens_number) + ' tokens'
    print 'FINISHED'

    t2 = time.time()
    print t2 - t1


if __name__ == '__main__':
    main()
