# -*- coding: utf-8 -*-
import urllib2
import re
import codecs
import HTMLParser
import os

hPrs = HTMLParser.HTMLParser()

visited = []
to_be_visited = []


def crawl_forward(link):
    """возвращает всю-всю страницу строкой"""
    infile = urllib2.urlopen(link)
    raw_text = infile.read()
    text = raw_text.decode("cp874")
    infile.close()
    #print text[:50]
    return text


def thaiize_text(unclear_text):
    """возвращает текст статьи на тайском"""
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
    links = re.findall(u'<a href="(articlecontent_desc.php\?article_id=.+?)">(.+?)</a>', text)

    for link in links:
        if link[0] in visited:
            continue
        else:
            if re.search(u'[ก-๛]', link[1]):
                to_be_visited.append(link[0])
                print u'dobavleno:', link[0]
    to_be_visited = set(to_be_visited)
    to_be_visited = list(to_be_visited)
    return to_be_visited

thai_texts = crawl_forward(u"http://www.mcu.ac.th/site/articlecontent.php")
visited.append(u"http://www.mcu.ac.th/site/articlecontent.php")
to_be_visited = check_links(thai_texts, visited, to_be_visited)

try:
    os.makedirs(u'./texts/')
except:
    pass

i = 1
for link in to_be_visited:
    if i > 20:
        break
    link = link.replace(u"http://", u"")
    # link = urllib2.quote(link.encode('cp874'))
    if u'www.mcu.ac.th/site' in link:
        link = u"http://" + link
    else:
        if link.startswith(u'articlecontent'):
            link = u"http://www.mcu.ac.th/site/" + link
        else:
            continue
    print link
    text = crawl_forward(link)
    visited.append(link)
    to_be_visited = check_links(thai_texts, visited, to_be_visited)
    final_txt = thaiize_text(text)
    if final_txt == '':
        continue
    filename = u'./texts/' + str(i) + ".txt"
    print str(i) + u" " + link
    i += 1
    outfile = codecs.open(filename, "w", "utf-8")
    outfile.write(u'###' + link + u'\n\n')
    outfile.write(final_txt)
    outfile.close()
    print u'zapisano'