# coding: utf-8
__author__ = u'Татьяна'

# скрипт для парсинга словаря с сайта thai-language.com

import os, re, codecs
import json
import HTMLParser

hPrs = HTMLParser.HTMLParser()

path_personal = u'/home/lizaku55/PycharmProjects/Thai/'
path = path_personal + u'letters'
files = os.listdir(u'letters')
barr = []
bdict = {}
for nomen in files:
    f = codecs.open(path + nomen, 'r', 'utf-8')
    dtext = f.read()
    dtext = hPrs.unescape(dtext)
    tokens = re.findall(u"<td class=th><a href='/id/(.+?)'>(.+?)</a></td><td>(.+?)<span class='tt'>(.)</span> (.+?)<span class='tt'>(.)</span> (.+?)<span class='tt'>(.)</span></td><td class=pos>(.+?)</td><td>(.+?)</td>", dtext)

    for i in tokens:
        arr = []
        for j in i:
            j = re.sub(u'<[^>]+>', u' ', j)
            arr.append(j)
        #print arr
        barr.append(arr)
        #print arr
for arr in barr:
    dictic = {}
    dictic[u'id'] = arr[0]
    pathic = u'words\\' + arr[0] + u'.html'
    fword = codecs.open(pathic, u'r', u'utf-8')
    wtwex = fword.read()
    wtwex = hPrs.unescape(wtwex)
    wordtoken = re.findall()
    dictic[u'transl'] = arr[-1]
    dictic[u'pos'] = arr[-2]
    if dictic[u'pos'] == 'example sentence':
        continue
    #dictic[u'compounds'] = ' '.join(arr[2:-2])
    if arr[1] in bdict:
        bdict[arr[1]].append(dictic)
    else:
        bdict[arr[1]] = [dictic]

out = codecs.open(u'outdict.json', u'w', u'utf-8')
#js = json.dumps(sorted(bdict), ensure_ascii=False)
js = json.dump(bdict, out, ensure_ascii=False, indent=2)
#print js
#out.write(js)
out.close()
