# -*- coding: utf-8 -*-
import lxml.etree
import codecs
import re
import os


# очистка от лишних тегов, замена спец. символов XML
def cleanXmlString(s):
    s = re.sub('^.+<\?.+>', '', s)
    arr = s.split('\n')
    xml_arr = ['<xml>']
    for line in arr:
        line = line.replace(u'&', u'&amp;')
        line = line.replace(u'()', u'')
        if line.startswith(u'<doc'):
            line = line[:5] + line[5:].replace(u'<', u'&lt;')
        elif line.startswith(u'</doc'):
            line = line[:6] + line[6:].replace(u'>', u'gt;')
        else:
            line = line.replace(u'<', u'&lt;')
            line = line.replace(u'>', u'&gt;')
        xml_arr.append(line)
    xml_arr.append('</xml>')
    clean_xml_string = '\n'.join([x for x in xml_arr])
    return clean_xml_string
    

# запись в файл XML
def writeToFile(xml_string):
    tree = lxml.etree.fromstring(xml_string)
    docs = tree.xpath('doc')
    for doc in docs:
        title = doc.get('title')
        link = doc.get('url')
        fin_arr = []
        if u':' not in unicode(title):
            fin_string = u'<xml>\n\t<meta>\n\t\t<link>' + unicode(link) + \
                        u'</link>\n\t\t<title>' + unicode(title) + \
                        u'</title>\n\t\t<genre>Encyclopedia</genre>\n\t</meta>' + \
                        u'\n\t<text>' + unicode(doc.text).replace('\n', '') + u'</text>\n</xml>'
            f = codecs.open('./results/' + unicode(title).replace('/', '') + '.xml', 'w', 'utf-8')
            f.write(fin_string)
        
        
def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.startswith('wiki_'):
                xml_file = codecs.open(root + os.sep + file, 'r', 'utf-8')
                xml_string = xml_file.read()
                xml_file.close()
                xml_string = cleanXmlString(xml_string)
                writeToFile(xml_string)
    print 'done'


if __name__ == main():
    main()