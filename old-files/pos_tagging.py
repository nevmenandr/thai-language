#-*- coding: utf-8 -*-

# скрипт для частеречной разметки тайского текста

import codecs, json, re

fj = codecs.open('/home/boris/Work/thai/thai_pos.json', 'r', 'utf-8')
d_pos = json.load(fj)
fj.close()

f = codecs.open('9.txt', 'r', 'utf-8')
fw = codecs.open('9_tagged.txt', 'w', 'utf-8')
for line in f:
    if u'###' in line:
        continue
    if re.search(u'[ก-๛]', line):
        line = line.strip()
        syllabs = line.split()
        line_mai = []
        for word in syllabs:
            if word in d_pos:
                fw.write(word + u'_' + d_pos[word] + u' ')
            else:
                fw.write(word + u'_bastard' + u' ')
    fw.write(u'\n')
f.close()
fw.close()
 
