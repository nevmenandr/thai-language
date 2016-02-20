#-*- coding: utf-8 -*-

# Этот скрипт нужен для транслитерации тайского текста в латиницу.
# Для работы нужен json с тайско-латинскими соответствиями

import codecs, json, re

fj = codecs.open('thai_consonants.json', 'r', 'utf-8')
d_cons = json.load(fj)
fj.close()

f = codecs.open('9.txt', 'r', 'utf-8')
fw = codecs.open('9_trans.txt', 'w', 'utf-8')
for line in f:
    if u'###' in line:
        continue
    if re.search(u'[ก-๛]', line):
        line = line.strip()
        syllabs = line.split()
        line_mai = []
        for syl in syllabs:
            syl_mai = u''
            for i in range(len(syl)):
                if syl[i] in d_cons:
                    ii = i
                    while ii >= 0:
                        if syl[ii] not in d_cons:
                            syl_mai += d_cons[syl[i]]['Final']
                            break
                        ii -= 1
                        if ii == -1:
                            syl_mai += d_cons[syl[i]]['Initial']
                else:
                    syl_mai += syl[i]
            line_mai.append(syl_mai)
        trnsl_line = u' '.join(line_mai)
        fw.write(trnsl_line + u'\n')
f.close()
fw.close()
 
