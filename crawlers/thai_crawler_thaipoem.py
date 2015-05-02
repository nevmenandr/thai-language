# -*- coding: utf-8 -*-
import urllib2
import re
import codecs
import HTMLParser
import os

hPrs = HTMLParser.HTMLParser()

#if re.search(u"[ก-๛]", token):

visited = []
to_be_visited = []

thaipoem_visited = []
thaipoem_to_be_visited = []

def crawl_forward(link):
    infile = urllib2.urlopen(link) 
    raw_text = infile.read()
    text = raw_text.decode("utf-8")
    infile.close()
    return text

def thaiize_text(unclear_text):
    thai_article = []
    lines = unclear_text.split('\n')
    fl = 0
    for line in lines:
        if '</div>' in line:
            fl = 0
        if fl == 1:
            line = hPrs.unescape(line)
            thai_article.append(line)
        if '<div class="article">' in line:
            fl = 1
    return '\n'.join(thai_article)

def thaipoem_parse(unclear_text):
    thai_article = []
    lines = unclear_text.split('\n')
    fl = 0
    for line in lines:
        if '</pre>' in line:
            fl = 0
        if fl == 1:
            line = hPrs.unescape(line)
            thai_article.append(line)
        if '<pre' in line:
            fl = 1
    return '\n'.join(thai_article)
            

def check_links(text, visited, to_be_visited):
    links = []
    if u"http://www.thaipoem.com/" in visited:
        links = re.findall(u' href="(.*/[0-9]*)"', text)
    if u"http://www.thaipoem.com/" in visited:
        links = re.findall(u' href="(.*?/Content/.*?)"', text)
    for link in links:
        if link in visited:
            continue
        else:
            if not u'img' in link:
                to_be_visited.append(link)
    to_be_visited = set(to_be_visited)
    to_be_visited = list(to_be_visited)
    return to_be_visited
    
#thai_texts = crawl_forward(u"http://www.dailynews.co.th/Content")
thaipoem_texts = crawl_forward(u"http://www.thaipoem.com/")

#visited.append(u"http://www.dailynews.co.th/Content")
#to_be_visited = check_links(thai_texts, visited, to_be_visited)

thaipoem_visited.append(u"http://www.thaipoem.com/")
thaipoem_to_be_visited = check_links(thaipoem_texts, thaipoem_visited, thaipoem_to_be_visited)

# i = 1
# for link in to_be_visited:
#     link = link.replace(u"http://", u"")
#     link = urllib2.quote(link.encode('utf-8'))
#     if u'www.dailynews.co.th' in link:
#         link = u"http://" + link
#     else:
#         if link.startswith( u'/Content/' ):
#             link = u"http://www.dailynews.co.th" + link
#         else:
#             continue
#     text = crawl_forward(link)
#     visited.append(link)
#     to_be_visited = check_links(thai_texts, visited, to_be_visited)
#     final_txt = thaiize_text(text)
#     filename = str(i) + ".txt"
#     print str(i) + u" " + link
#     i+=1
#     if not os.path.exists(u'thai_dailynews2/'):
#         os.makedirs(u'thai_dailynews2/')
#     outfile = codecs.open(u"thai_dailynews2/" + filename, "w", "utf-8")
#     title = ''
#     initial_str = u'<?xml version="1.0" encoding="UTF-8"?>\n<meta><link>' + link + u'</link>\n' +\
#               u'<title>' + title + u'</title>\n<genre>paper</genre></meta>\n<text>\n'
#     outfile.write(initial_str)
#     #outfile.write(u'###' + link + u'\n\n')
#     outfile.write(final_txt)
#     outfile.close()

i = 1
for link in thaipoem_to_be_visited:
    link = link.replace(u"http://", u"")
    link = urllib2.quote(link.encode('utf-8'))
    if u'www.thaipoem.com' in link:
        link = u"http://" + link
    text = crawl_forward(link)
    thaipoem_visited.append(link)
    thaipoem_to_be_visited = check_links(thaipoem_texts, thaipoem_visited, thaipoem_to_be_visited)
    final_txt = thaipoem_parse(text)
    filename = str(i) + ".txt"
    print str(i) + u" " + link
    i+=1
    if not os.path.exists(u'thaipoem/'):
        os.makedirs(u'thaipoem/')
    outfile = codecs.open(u"thaipoem/" + filename, "w", "utf-8")
    title = ''
    initial_str = u'<?xml version="1.0" encoding="UTF-8"?>\n<meta><link>' + link + u'</link>\n' +\
              u'<title>' + title + u'</title>\n<genre>paper</genre></meta>\n<text>\n'
    outfile.write(initial_str)
    #outfile.write(u'###' + link + u'\n\n')
    outfile.write(final_txt)
    outfile.close()

