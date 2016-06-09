# -*- coding: utf-8 -*-

import os
import time
import shutil
# import random

__author__ = 'gree-gorey'


def copy(path, path_to_write, folder_limit, limit):
    i = 0
    # собираем все папки разных ресурсов
    sources = []
    for root, dirs, files in os.walk(path):
        for source in dirs:
            sources.append(os.path.join(root, source))

    # обходим все эти папки по очереди
    for source in sources:
        # рекурсивно обходим папку
        for root, dirs, files in os.walk(source):
            # if len(files) > folder_limit:
            #     files = random.sample(files, folder_limit)
            for filename in files:
                open_name = os.path.join(root, filename)
                write_name = open_name.replace(path, path_to_write)
                shutil.copy(open_name, write_name)
                i += 1
                print round(float(i) / limit * 100, 3), "% complete...         \r",

            break

    print ''


def calculate(path, limit):
    number_of_sources = 1
    for root, dirs, files in os.walk(path):
        number_of_sources = len(dirs)
        break
    return int(float(limit) / number_of_sources)
    # files_total = int(commands.getstatusoutput('find . -type f | wc -l')[1])


def create_empty_folder_tree(open_root, write_root):
    for root, dirs, files in os.walk(open_root):
        for directory in dirs:
            path_to_dir = os.path.join(root, directory).replace(open_root, write_root)
            if not os.path.exists(path_to_dir):
                os.makedirs(path_to_dir)


def main():
    t1 = time.time()

    limit = 50000

    open_root = '../dummy_texts/'
    write_root = '../new/'

    create_empty_folder_tree(open_root, write_root)

    tokens_per_source = calculate(open_root, limit)

    print tokens_per_source

    copy(open_root, write_root, files_per_source, limit)

    print 'FINISHED'

    t2 = time.time()
    print t2 - t1


if __name__ == '__main__':
    main()