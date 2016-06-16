# Delete one of the duplicate meanings of a word from the dictionary

import codecs
from collections import Counter
import json
import re

f = codecs.open('slovar.json', 'r', 'utf-8')
text = f.read()
f.close()
slovar = json.loads(text)

global old_meanings
old_meanings = []

def clean(slovar):
    old = 0
    for s in slovar:
        meanings = {}
        for l in slovar[s]:
            meanings[l] = (slovar[s][l][0])
        old += len(meanings)
        if len(meanings) > 1:
            values = []
            for m in meanings:
                split_m = meanings[m].split(';')
                if len(split_m) > 1:
                    for spl in split_m:
                        values.append(spl.lstrip())
                if meanings[m].startswith("[Thai transcription"):
                    new = re.findall("Thai transcription .+? \"(.+?)\"", meanings[m], flags=re.U)
                    if len(new) > 0:
                        meanings[m] = new[0]
                values.append(meanings[m])
            ununique_values = [k for (k,v) in Counter(values).iteritems() if v > 1]
            if len(ununique_values) > 0:
                for u in ununique_values:
                    for l in slovar[s]:
                        if u == slovar[s][l][0]:
                            del slovar[s][l]
                            break
    old_meanings.append(old)
    for s in slovar:
        meanings = {}
        for l in slovar[s]:
            meanings[l] = (slovar[s][l])
        del slovar[s]
        slovar[s] = {}
        n = 1
        for m in meanings:
            slovar[s][n] = meanings[m]
            n += 1

    return slovar

old = 0
for s in slovar:
    meanings = {}
    for l in slovar[s]:
        meanings[l] = (slovar[s][l][0])
    old += len(meanings)
old_meanings.append(old)

new_meanings = 0

while old_meanings[-1] != new_meanings:
    slovar = clean(slovar)
    new_meanings = 0
    for s in slovar:
        meanings = {}
        for l in slovar[s]:
            meanings[l] = (slovar[s][l][0])
        new_meanings += len(meanings)

new_meanings = 0
for s in slovar:
    meanings = {}
    for l in slovar[s]:
        meanings[l] = (slovar[s][l][0])
    new_meanings += len(meanings)

print u'There were ' + str(old_meanings[0] - new_meanings) + u' meanings deleted.'

new_slovar = json.dumps(slovar, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
f = codecs.open(u'new_slovar.json', 'w', 'utf-8')
f.write(new_slovar)
f.close()
    
            
                
                        
                        
                



    
