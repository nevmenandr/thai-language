#Надо подправить!!

import codecs
import operator
import os
import re

freq = {}

pages = os.listdir('./corpora')

for page in pages:
    f = codecs.open(u'C:/Users/M/Desktop/corpora/' + page, 'r', 'utf-8')
    text = f.read()
    f.close()
    words = text.split(u'|')
    for word in words:
        if word.startswith(u'<'):
            word = word[4:-6]
        if word in freq:
            freq[word] += 1
        if word not in freq:
            freq[word] = 1

f = codecs.open(u'Word frequency.txt', 'w', 'utf-8')

for word in reversed(sorted(freq, key=freq.get)):
    line = word + u' - ' + str(freq[word])
    if line == u'':
        breal
    f.write(line)
    f.write(os.linesep)
