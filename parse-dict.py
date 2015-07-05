# coding: utf-8
__author__ = u'Татьяна'

# скрипт для парсинга словаря с сайта thai-language.com

import os, re, codecs
import json
import HTMLParser

hPrs = HTMLParser.HTMLParser()

path_local = u'/home/lizaku55/PycharmProjects/Thai/thai_dict/'
path_let = path_local + u'letters/'
files = os.listdir(path_let)
barr = []
bdict = {}
for nomen in files:
    f = codecs.open(path_let + nomen, 'r', 'utf-8')
    dtext = f.read()
    dtext = hPrs.unescape(dtext)
    entries = re.findall(u"<td class=th>.*?</tr>", dtext)
    for entry in entries:
        id = re.findall('<a href=[\'"]([^\'"]*)', re.findall(u'<td[^>]*>(.*?)</td>', entry)[0])[0].split('/')[-1][:6]
        tokens = [re.sub('<[^>]*>', '', x) for x in re.findall(u'<td[^>]*>(.*?)</td>', entry)]
        tokens.append(id)
        barr.append(tokens)

    #for i in tokens:
    #    print i.replace('\r', '').replace('\n', '').replace('\t', '')
    #    arr = []
    #    for j in i:
    #        j = re.sub(u'<[^>]+>', u' ', j)
    #        arr.append(j)
    #    #print arr
    #    barr.append(arr)
    #    #print arr

for tokens in barr:
    dictic = {}
    dictic[u'id'] = tokens[4]
    dictic[u'token'] = tokens[0]
    dictic[u'transl'] = tokens[3]
    dictic[u'pos'] = tokens[2]
    dictic[u'transcr'] = tokens[1]

    ## NOT READY YET!
    #path_word = path_local + u'words/' + tokens[4] + u'.html'
    #try:
    #    fword = codecs.open(path_word, u'r', u'utf-8')
    #    wtwex = fword.read()
    #    wtwex = hPrs.unescape(wtwex)
    #    wentries = re.findall(u"<td class=th>.*?</tr>", wtwex)
        #for wentry in wentries:
            #wtokens = re.findall(u'<td[^>]*>(.*?)</td>', wentry)
            #print wtokens
    #except:
    #    pass
    if tokens[0] in bdict:
        bdict[tokens[0]].append(dictic)
    else:
        bdict[tokens[0]] = [dictic]

out = codecs.open(path_local + u'outdict.json', u'w', u'utf-8')
#js = json.dumps(sorted(bdict), ensure_ascii=False)
js = json.dump(bdict, out, ensure_ascii=False, indent=2)
#print js
#out.write(js)
out.close()
