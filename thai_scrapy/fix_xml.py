# -*- coding:utf-8 -*-

import time
import codecs
import os

__author__ = 'gree-gorey'


def texts(path, new_path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = path + filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                lines = f.readlines()
                try:
                    if lines[1] != u'<xml>\n':
                        lines.insert(1, u'<xml>\n')
                        lines.insert(10, u'\n</xml>')
                except:
                    pass
            write_name = new_path + filename
            with codecs.open(write_name, u'w', u'utf-8') as w:
                w.write(u''.join(lines))


def main():
    t1 = time.time()

    texts(u'./to_fix/', u'./new/')

    t2 = time.time()
    print t2 - t1


if __name__ == '__main__':
    main()
