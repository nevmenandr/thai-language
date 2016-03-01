#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys, os
import urllib2
import unittest
import mega_crawler

__author__ = 'Gree-gorey'


class TestUserAgent(unittest.TestCase):
    def setUp(self):
        self.crawler = mega_crawler.UserAgent()

    def tearDown(self):
        pass

    def test_default_agentname(self):
        """
        Если имя не задано в конструкторе, он должно соответствовать
        имени по умолчанию.
        """
        msg = "Default agent name should be '%s', not '%s'" % \
            (mega_crawler.DEFAULT_AGENTNAME, self.crawler.agentname)
        self.assertEqual(self.crawler.agentname, mega_crawler.DEFAULT_AGENTNAME, msg)

    def test_custom_agentname(self):
        """
        Если имя задано в конструкторе, оно должно таким и быть.
        """
        name = 'Other Test/2.0'
        c = mega_crawler.UserAgent(agentname=name)
        self.assertEqual(
        c.agentname,
        name,
        "Custom agent name should be '%s', not '%s'" % \
        (name, c.agentname))

    def test_htmlget(self):
        """
        Краулер открывает заданный ресурс и в заголовке ответа возвращается
        text/html.
        """
        resp = self.crawler.open('http://spintongues.msk.ru/kafka2.html')
        ctype = resp.info().get('Content-Type')
        # В заголовке может быть что-нибудь вроде 'text/html; charset=windows-1251',
        # поэтому обычное сравнение не подходит.
        self.assert_(ctype.find('text/html') != -1, 'Not text/html')

    def test_urlerror(self):
        """
        Если задан неверный адрес, должны генерироваться ошибка IOError.
        """
        self.assertRaises(IOError, self.crawler.open, 'http://foo/bar/buz/a765')

    def test_robotrules(self):
        """
        Если выяснилось, что robots.txt запрещает посещение адреса,
        должно генерироваться исключение.
        """
        # Яндекс, как известно, не любит пауков
        self.assertRaises(RuntimeError, self.crawler.open, 'http://yandex.ru/')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserAgent)
    unittest.TextTestRunner(verbosity=2).run(suite)
