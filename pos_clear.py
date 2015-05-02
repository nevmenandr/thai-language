# скрипт очищает результаты pos_finder.py

import os
import codecs

pos_list = []

text = codecs.open(u'/Users/apple/Desktop/pos_list.txt', 'r', 'utf-8')
for pos in text:
    pos = pos.strip()
    if ',' in pos:
        pos_clear = pos.split(', ')
        pos_list.extend(pos_clear)
    else:
        pos_list.append(pos)

text.close()


pos_list_clear = set(pos_list)

outfile = codecs.open('/Users/apple/Desktop/real_pos_list.txt', 'w', 'utf-8')
pos_list_clear = list(pos_list_clear)

for pos in sorted(pos_list_clear):
    outfile.write(pos + '\n')

outfile.close()
