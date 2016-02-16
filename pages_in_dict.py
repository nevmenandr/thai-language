import codecs
import os
import re

letters = []
no_letters = []
number_of = {}
existing_pages = {}
nonexistent_pages = {}

pages = os.listdir("./pages")


for page in pages:
    if page.endswith('.html'):
        if page[0:3] not in letters:
            letters.append(page[0:3])
        name = u'C:/Users/M/Desktop/Thai/pages/' + page
        f = codecs.open(name, 'r', 'utf-8-sig')
        text = f.read()
        n = re.findall('Page ([0-9]+?) of ([0-9]+?)\\.', text, flags=re.U)
        number_of[page[0:3]] = n[0][1]
        if page[0:3] in existing_pages:
            existing_pages[page[0:3]].append(n[0][0])
        else:
            existing_pages[page[0:3]] = [n[0][0]]

for i in range(161, 206):
    if str(i) not in letters:
        no_letters.append(str(i))

for l in letters:
    total = number_of[l]
    for i in range(2, int(total)):
        if l not in existing_pages:
            print u'Page ' + l + u' is not in existing pages. Why?'
        else:
            if str(i) not in existing_pages[l]:
                if l in nonexistent_pages:
                    nonexistent_pages[l].append(str(i))
                else:
                    nonexistent_pages[l] = [str(i)]

print u'There are no pages with these letters:'
for nl in no_letters:
    print nl + u' ',

print u''
print u''
print u'And the following letters miss the noted pages'

for np in nonexistent_pages:
    print u''
    print u'Page ' + np
    print u''
    for i in nonexistent_pages[np]:
        print i + u' ',
    print u''


    
        
    

