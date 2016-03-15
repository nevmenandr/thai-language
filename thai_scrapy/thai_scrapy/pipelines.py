# -*- coding: utf-8 -*-

import codecs


class XMLPipeline(object):

    def process_item(self, item, spider):
        with codecs.open(u'./output/' + str(item[u'name']) + u'.xml', u'w', u'utf-8') as f:
            text = u'<?xml version="1.0" encoding="UTF-8"?>\n<xml>\n' \
                   u'<meta>\n<link>' + item[u'link'] + u'</link>\n' +\
                   u'<title>' + item[u'title'] + u'</title>\n<genre>paper</genre>\n</meta>\n<text>\n' + \
                   item[u'content'] + u'\n</text>\n</xml>'
            f.write(text)
        return item
