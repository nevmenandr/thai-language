# -*- coding: utf-8 -*-

import re
import codecs
import os
os.environ['http_proxy']=''
import HTMLParser
import urllib2

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
    title = u''
    for line in lines:
        if re.search(u'<title>.+?(\(.+\))</title>', line):
            s = re.search(u'<title>.+?\((.+)\)</title>', line)
            title = s.group(1)
            thai_article.append(title)
        elif re.search(u'<title>.+?</title>', line):
            s = re.search(u'<title>.+?</title>', line)
            title = s.group()
            thai_article.append(title)
        if '</div>' in line:
            fl = 0
        if fl == 1:
            line = hPrs.unescape(line)
            thai_article.append(line)
        if '<div class="post-content">' in line:
            fl = 1
    return thai_article, title


def clearing(thai_article):
    latin = u'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    #latin = list(latin)
    clear_thai = []
    for line in thai_article:
        mot = 0
        line = re.sub(u'<.+?>', u'', line)
        for letter in line:
            if letter in latin:
                mot = 1
        if mot == 0:
            clear_thai.append(line)
    return '\n'.join(clear_thai)


def check_links(text, visited, to_be_visited):
    #links = re.findall(u'href="(http://www.nithan.in.th/%e.*?)"', text)
    links = re.findall(u'href="(http://www.nithan.in.th/[a-z\-]*?%e.*?)"', text)
    for link in links:
        if link in visited:
            continue
        else:
            to_be_visited.append(link)
    to_be_visited = set(to_be_visited)
    to_be_visited = list(to_be_visited)
    return to_be_visited


def searching(mass, nazv):
    massivstranic = []
    to_be_visited = []
    try:
        os.makedirs(u'./' + nazv)
    except:
        pass
    dsg = {u'Сказки Эзопа/': u'Aesop', u'Английские сказки/': u'Engl', u'Народные сказки/' : u'Folk', u'Стиль жизни/' : u'LifeStyle'}
    for ssy in mass:
        massivstranic.append(crawl_forward(ssy))
    for item in massivstranic:
        to_be_visited = check_links(item, visited, to_be_visited)
        print u'Собрали ссылочки с'
    i = 1
    for link in to_be_visited:
        # if i > 5:
        #     break
        print u'Зашли в гости'
        #link = link.replace(u"http://", u"")
        #link = urllib2.quote(link.encode('utf-8'))
        #link = u"http://" + link
        text = crawl_forward(link)
        visited.append(link)
        #to_be_visited = check_links(thai_texts, visited, to_be_visited)
        final_txt, title = thaiize_text(text)
        final_txt = clearing(final_txt)
        final_txt += u'\n</text>'
        #final_txt='\n'.join(final_txt)
        filename = str(i) + ".txt"
        print str(i) + u" " + link
        i+=1
        outfile = codecs.open(nazv + filename, "w", "utf-8")
        initial_str = u'<?xml version="1.0" encoding="UTF-8"?>\n<meta><link>' + link + u'</link>\n<title>' + title + u'</title>\n<genre>fairytale</genre><subgenre>' + dsg[nazv] + '</subgenre></meta>\n<text>\n'
        outfile.write(initial_str)
        #outfile.write(u'<?xml version = "1.0" encoding = "UTF-8"?>\n<linc' + link + u'\n\n')
        outfile.write(final_txt)
        outfile.close()
        print u'Одна сказка!', i

print u'Start'
thai_texts1 = u"http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%AD%E0%B8%B5%E0%B8%AA%E0%B8%9B"

thai_texts2 = u"http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%AD%E0%B8%B5%E0%B8%AA%E0%B8%9B/page/2"

thai_texts3 = u"http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%AD%E0%B8%B5%E0%B8%AA%E0%B8%9B/page/3"

thai_texts4 = u"http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%AD%E0%B8%B5%E0%B8%AA%E0%B8%9B/page/4"

thai_texts5 = u"http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%AD%E0%B8%B5%E0%B8%AA%E0%B8%9B/page/5"

visited.append(u"http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%AD%E0%B8%B5%E0%B8%AA%E0%B8%9B")

mass = [thai_texts1, thai_texts2, thai_texts3, thai_texts4, thai_texts5]
mass2 = [u'http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B2%E0%B8%AD%E0%B8%B1%E0%B8%87%E0%B8%81%E0%B8%A4%E0%B8%A9', u'http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%A0%E0%B8%B2%E0%B8%A9%E0%B8%B2%E0%B8%AD%E0%B8%B1%E0%B8%87%E0%B8%81%E0%B8%A4%E0%B8%A9/page/2']
mass3 = [u'http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%9E%E0%B8%B7%E0%B9%89%E0%B8%99%E0%B8%9A%E0%B9%89%E0%B8%B2%E0%B8%99', u'http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%9E%E0%B8%B7%E0%B9%89%E0%B8%99%E0%B8%9A%E0%B9%89%E0%B8%B2%E0%B8%99/page/2']
mass4 = [u'http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%8A%E0%B8%B2%E0%B8%94%E0%B8%81', u'http://www.nithan.in.th/category/%E0%B8%99%E0%B8%B4%E0%B8%97%E0%B8%B2%E0%B8%99%E0%B8%8A%E0%B8%B2%E0%B8%94%E0%B8%81/page/2']
'''
for item in massivstranic:
    to_be_visited = check_links(item, visited, to_be_visited)
    print u'Собрали ссылочки с'
i = 1
for link in to_be_visited:
    print u'Зашли в гости'
    #link = link.replace(u"http://", u"")
    #link = urllib2.quote(link.encode('utf-8'))
    #link = u"http://" + link
    text = crawl_forward(link)
    visited.append(link)
    #to_be_visited = check_links(thai_texts, visited, to_be_visited)
    final_txt, title = thaiize_text(text)
    final_txt = clearing(final_txt)
    #final_txt='\n'.join(final_txt)
    filename = str(i) + ".txt"
    print str(i) + u" " + link
    i+=1
    outfile = codecs.open(u"thai_skaz/" + filename, "w", "utf-8")
    initial_str = u'<?xml version="1.0" encoding="UTF-8"?>\n<meta><link>' + link + u'</link>\n' + title + u'\n<genre>fairytale</genre></meta>\n<text>\n'
    outfile.write(initial_str)
    #outfile.write(u'<?xml version = "1.0" encoding = "UTF-8"?>\n<linc' + link + u'\n\n')
    outfile.write(final_txt)
    outfile.close()
    print u'Одна сказка!', i
'''
searching(mass, u"Сказки Эзопа/")
searching(mass2, u'Английские сказки/')
searching(mass3, u'Народные сказки/')
searching(mass4, u'Стиль жизни/')

print u'Finish'
