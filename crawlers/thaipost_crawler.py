# -*- coding: utf-8 -*-
import urllib2
import re
import codecs
import HTMLParser

hPrs = HTMLParser.HTMLParser()

visited = []
to_be_visited = []

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
        if '<div class="field-items"><div class="field-item even" property="content:encoded">' in line:
            fl = 1
    return '\n'.join(thai_article)
            
        

def check_links(text, visited, to_be_visited):
    links = re.findall(u' href="(.+?q=.+?)"', text)
    for link in links:
        if link in visited:
            continue
        else:
            to_be_visited.append(link)
    to_be_visited = set(to_be_visited)
    to_be_visited = list(to_be_visited)
    return to_be_visited
    
thai_texts = crawl_forward(u"http://www.thaipost.net/")
# print thai_texts
visited.append(u"http://www.thaipost.net/")
to_be_visited = check_links(thai_texts, visited, to_be_visited)
i = 1
for link in to_be_visited:
    print link
    link = link.replace(u"http://", u"")
    link = urllib2.quote(link.encode('utf-8'))
    if u'www.thaipost.net' in link:
        link = u"http://" + link
        print link
    else:
        if re.search('q=[ก-๛]', link) is not None:
            link = u"http://www.thaipost.net" + link
        else:
            continue
    text = crawl_forward(link)
    title = re.findall('<title>([^<]*)</title>', text, flags=re.U)[0]
    visited.append(link)
    to_be_visited = check_links(thai_texts, visited, to_be_visited)
    final_txt = thaiize_text(text)
    filename = "thaipost.net/" + str(i) + ".xml"
    print str(i) + u" " + link
    i+=1
    outfile = codecs.open(filename, "w", "utf-8")
    initial_str = u'<?xml version = "1.0" encoding = "UTF-8"?>\n<meta><link>' + link +\
                  u'</link>\n' + u'<title>' + title + u'</title>\n<genre>paper</genre></meta>\n<text>\n'
    outfile.write(initial_str)
    outfile.write(final_txt)
    outfile.close()
