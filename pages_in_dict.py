import codecs
import os
import re
import urllib2

letters = []
one_page_letters = []
number_of = {}
existing_pages = {}
nonexistent_pages = {}

pages = os.listdir('./pages')

for page in pages:
    if page.endswith('.html'):
        if page[0:3] not in letters:
            letters.append(page[0:3])
        name = u'C:/Users/M/Desktop/Thai/pages/' + page
        f = codecs.open(name, 'r', 'utf-8-sig')
        text = f.read()
        f.close()
        n = re.findall('Page ([0-9]+?) of ([0-9]+?)\\.', text, flags=re.U)
        number_of[page[0:3]] = n[0][1]
        if page[0:3] in existing_pages:
            existing_pages[page[0:3]].append(n[0][0])
        else:
            existing_pages[page[0:3]] = [n[0][0]]


for i in range(161, 206):
    if str(i) not in letters:
        one_page_letters.append(str(i))
    

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


#print u'And the following pages are not downloaded:'

for np in nonexistent_pages:
    print u''
    print u'Page ' + np
    print u''
    for i in nonexistent_pages[np]:
        print i + u' ',
#    print u''

exact_urls = []

for np in nonexistent_pages:
    for p in nonexistent_pages[np]:
        url = u'http://www.thai-language.com/let/' + np + u'.' + p
        print url
        exact_urls.append(url)

starting_urls = []

for nl in no_letters:
    starting_urls.append(u'http://www.thai-language.com/let/' + nl + u'.2')
        
#for eu in exact_urls:
    #infile = urllib2.urlopen(eu) 
    #raw_text = infile.read()
    #text = raw_text.decode("utf-8")
    #name = u'C:/Users/M/Desktop/Thai/pages/' + eu[33:] + u'.html'
    #f = codecs.open(name, 'w', 'utf-8-sig')
    #f.write(text)
    #f.close()

#for su in starting_urls:
    #infile = urllib2.urlopen(su) 
    #raw_text = infile.read()
    #text = raw_text.decode("utf-8")
    #name = u'C:/Users/M/Desktop/Thai/pages/' + su[33:] + u'.html'
    #f = codecs.open(name, 'w', 'utf-8-sig')
    #f.write(text)
    #f.close()








    
        
    

