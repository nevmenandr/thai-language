# -*- coding: utf-8 -*-
# This version needs no wget

import urllib2
import re
import codecs
import HTMLParser
import os

hPrs = HTMLParser.HTMLParser()

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


def thaipoem_parse(unclear_text):
    thai_article = ''
    find_text = re.findall(u'<p>(.*?)</p>', unclear_text, re.DOTALL)
    if find_text is not None:
        for p in find_text:
            thai_article += p + '\n'
    return thai_article

def check_links(text, visited, to_be_visited):
    links = []
    if u"http://www.thairath.co.th/ent/novel" in visited:
        links = re.findall(u' href="(/ent/novel/.*?)"', text)
    for link in links:
        if link in visited:
            continue
        else:
            if not u'img' in link:
                to_be_visited.append(u"http://www.thairath.co.th" + link)
    to_be_visited = set(to_be_visited)
    to_be_visited = list(to_be_visited)
    return to_be_visited

thaipoem_texts = crawl_forward(u"http://www.thairath.co.th/ent/novel")

thaipoem_visited.append(u"http://www.thairath.co.th/ent/novel")
thaipoem_to_be_visited = check_links(thaipoem_texts, thaipoem_visited, thaipoem_to_be_visited)
i = 1
for link in thaipoem_to_be_visited:
    if i > 5:
        break
    link = link.replace(u"http://", u"")
    link = urllib2.quote(link.encode('utf-8'))
    if u'www.thairath.co.th/ent/novel' in link:
        link = u"http://" + link
    text = crawl_forward(link)
    thaipoem_visited.append(link)
    thaipoem_to_be_visited = check_links(thaipoem_texts, thaipoem_visited, thaipoem_to_be_visited)
    final_txt = thaipoem_parse(text)
    filename = str(i) + ".txt"
    print str(i) + u" " + link
    i+=1
    if not os.path.exists(u'thairath/'):
        os.makedirs(u'thairath/')
    outfile = codecs.open(u'thairath/' + filename, "w", "utf-8")
    title = ''
    initial_str = u'<?xml version="1.0" encoding="UTF-8"?>\n<meta><link>' + link + u'</link>\n' +\
              u'<title>' + title + u'</title>\n<genre>poem</genre></meta>\n<text>\n'
    outfile.write(initial_str)
    outfile.write(final_txt)
    outfile.close()
