import codecs
import os
import re

letters = []
no_letters = []
number_of = {}

pages = os.listdir(".")


for page in pages:
    if page.endswith('.html'):
        if page[0:3] not in letters:
            letters.append(page[0:3])
        f = codecs.open(page, 'r', 'utf-8-sig')
        text = f.read()
        #n = re.findall('Page [0-9]*? of [0-9][0-9]', text, flags=re.U)
        #number_of[page[0:3]] = n[-1:-2]

for i in range(161, 206):
    if str(i) not in letters:
        no_letters.append(str(i))

print no_letters
