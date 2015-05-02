# -*- coding: utf-8 -*-
import urllib2
import re
import codecs
import HTMLParser

hPrs = HTMLParser.HTMLParser()

#if re.search(u"[ก-๛]", token):

regTitle = re.compile(u'<h1 class="entry-title">(.*?)</h1>', flags=re.U | re.DOTALL)
regArticle = re.compile(u'<div class="entry">(.*?)</div>', flags=re.U | re.DOTALL)
regTag = re.compile(u'<.*?>', flags=re.U | re.DOTALL)
visited = []
to_be_visited = []
categories = 'royalnews|politics|article|bangkok|pr|women|education|crime|regional|foreign|sports|it|entertainment|economic|agriculture'

def crawl_forward(link):
    infile = urllib2.urlopen(link) 
    raw_text = infile.read()
    text = raw_text.decode("utf-8")
    infile.close()
    return text


def thaiize_text(unclear_text):
    title = regTitle.search(unclear_text).group(1)
    text = regArticle.search(unclear_text).group(1).replace('<p>', '\n').replace('</p>', '\n')
    text = re.sub(u'(\n)+', '\n', regTag.sub('', text))
    return hPrs.unescape(title), hPrs.unescape(text)


def check_links(text, visited, to_be_visited):
    links = re.findall(u'a href="(/(?:' + categories + ')/.*?)"', text)
    for link in links:
        if link in visited:
            continue
        else:
            to_be_visited.append(link)
    to_be_visited = list(set(to_be_visited))
    return to_be_visited
    
thai_texts = crawl_forward(u"http://www.dailynews.co.th")
visited.append(u"http://www.dailynews.co.th")
to_be_visited = check_links(thai_texts, visited, to_be_visited)
i = 1
for link in to_be_visited:
    print link
    if i > 10:
        break
    link = link.replace(u"http://", u"")
    link = urllib2.quote(link.encode('utf-8'))
    link = u"http://www.dailynews.co.th" + link
    text = crawl_forward(link)
    visited.append(link)
    to_be_visited = check_links(thai_texts, visited, to_be_visited)
    final_txt = thaiize_text(text)
    filename = str(i) + ".txt"
    print str(i) + u" " + link
    i+=1
    initial_str = u'<?xml version="1.0" encoding="UTF-8"?>\n<meta><link>' + link + u'</link>\n' +\
              u'<title>' + final_txt[0] + u'</title>\n<genre>paper</genre></meta>\n<text>\n' + final_txt[1]
    outfile = codecs.open(filename, "w", "utf-8")
    outfile.write(initial_str + '</text>')
    outfile.close()

