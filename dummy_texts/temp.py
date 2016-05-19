# -*- coding: utf-8 -*-

import os
import codecs
from lxml import etree
import pythai

__author__ = 'gree-gorey'


def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = path + filename
            print filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                tree = etree.parse(f)
            return tree, filename


def pos(string):
    tokens = pythai.split(string)
    return tokens


def sentence_iterator(text):
    sentences = text.split(u' ')
    for sentence in sentences:
        clear_sentence = u''
        previous_not_thai = False
        for i, char in enumerate(sentence):
            if 3585 <= ord(char) <= 3675:
                if previous_not_thai:
                    clear_sentence += u' '
                clear_sentence += char
                previous_not_thai = False
            else:
                if not previous_not_thai:
                    clear_sentence += u' '
                clear_sentence += char
                previous_not_thai = True
        yield clear_sentence


def main():
    tree, filename = read_xml(u'./corpus_from_tagged/')
    se = tree.xpath('//meta/link')
    print filename
    print se[0].text
    # print pos(u'¯°.¸♥♥¯° ศรรกรา ¯°.¸♥♥¯°what°¯♥♥¸.°´¯')
    # print ord(u'๛')
    # text = u'¯°.¸♥♥¯°ศรรกราหน้าทะเล้น°¯♥♥¸.°´¯'
    # for sentence in sentence_iterator(text):
    #     print pos(sentence)

if __name__ == '__main__':
    main()
