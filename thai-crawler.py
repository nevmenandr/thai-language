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
        if '<div class="article">' in line:
            fl = 1
    return '\n'.join(thai_article)
            
        

def check_links(text, visited, to_be_visited):
    links = re.findall(u' href="(.*?/Content/.*?)"', text)
    for link in links:
        if link in visited:
            continue
        else:
            to_be_visited.append(link)
    to_be_visited = set(to_be_visited)
    to_be_visited = list(to_be_visited)
    return to_be_visited
    
thai_texts = crawl_forward(u"http://www.dailynews.co.th/Content")
visited.append(u"http://www.dailynews.co.th/Content")
to_be_visited = check_links(thai_texts, visited, to_be_visited)
i = 1
for link in to_be_visited:
    link = link.replace(u"http://", u"")
    link = urllib2.quote(link.encode('utf-8'))
    if u'www.dailynews.co.th' in link:
        link = u"http://" + link
    else:
        if link.startswith( u'/Content/' ):
            link = u"http://www.dailynews.co.th" + link
        else:
            continue
    text = crawl_forward(link)
    visited.append(link)
    to_be_visited = check_links(thai_texts, visited, to_be_visited)
    final_txt = thaiize_text(text)
    filename = str(i) + ".txt"
    print str(i) + u" " + link
    i+=1
    outfile = codecs.open(u"/home/boris/Work/thai/spider/thai_dailynews2/" + filename, "w", "utf-8")
    outfile.write(u'###' + link + u'\n\n')
    outfile.write(final_txt)
    outfile.close()

