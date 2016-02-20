# поиск частей речи в html-страницах словаря thai-dictionary.com

import os
import codecs
import re

pages_path = u'/Users/apple/Downloads/thai_dictionary_site/pages/'
pages_names = os.listdir(pages_path)
pos_list = []

for page in pages_names:
    f = codecs.open(pages_path + page, "r", "utf-8")
    f_content = f.read()
    f.close()
    f_lines = f_content.split('<tr>')
    for f_line in f_lines:
        if "<a href='/id/" in f_line:
            pre_pos = re.search('class=pos>(.+?)<', f_line)
            if pre_pos:
                pos = pre_pos.group(1)
                pos_list.append(pos)

pos_list_clear = set(pos_list)

outfile = codecs.open(u'/Users/apple/Desktop/pos_list.txt', 'w', 'utf-8')
pos_list_clear = list(pos_list_clear)

for pos in sorted(pos_list_clear, key=len):
    outfile.write(pos + "\n")

outfile.close()
