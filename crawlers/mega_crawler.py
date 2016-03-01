#!/usr/bin/python
# -*- coding: cp1251 -*-

import sys
import urllib2
from copy import copy
from robotparser import RobotFileParser

'''
здесь будет универсальный краулер

начнем отсюда:
http://www.mcu.ac.th/site/articlecontent.php
'''

__author__ = 'Gree-gorey'

# Конфигурация по умолчанию
# TODO: вынести в конфигурационный файл
TIMEOUT = 5 # максимальное время ожидания ответа в секундах

# HTTP-заголовки, которые используются по умолчанию и могут быть
# переопределены в конструкторе UserAgent
DEFAULT_HEADERS = {
'Accept'           : 'text/html, text/plain',
'Accept-Charset'   : 'windows-1251, koi8-r, UTF-8, iso-8859-1, US-ASCII',
'Content-Language' : 'ru,en',
}
# Имя для HTTP-заголовка 'User-Agent' и проверки robots.txt
DEFAULT_AGENTNAME = 'Test/1.0'
# email автора; при пустом значении не используется
DEFAULT_EMAIL = ''


class RobotsHTTPHandler(urllib2.HTTPHandler):
    """
    Класс, который передается специализированному экземпляру
    OpenDirector.
    Прежде, чем произвести запрос, проверяет, нет ли запрета
    на посещение ресурса файлом robots.txt.

    Аргументы:
    agentname -- имя краулера
    """
    # TODO: кэшировать один раз полученные данные, чтобы при повторных
    #       запросах к одному хосту не делать лишних запросов.
    def __init__(self, agentname, *args, **kwargs):
     urllib2.HTTPHandler.__init__(self, *args, **kwargs)
     self.agentname = agentname

def http_open(self, request):
     """
     перегрузка родительского метода. Если в корне сервера
     имеется robots.txt c запретом на посещение заданного
     ресурса, генерируется исключение RuntimeError.

     request -- экземпляр urllib2.Request
     """
     url = request.get_full_url()
     host = urlsplit(url)[1]
     robots_url = urlunsplit(('http', host, '/robots.txt', '', ''))
     rp = RobotFileParser(robots_url)
     rp.read()
     if not rp.can_fetch(self.agentname, url):
         # запрещено
         raise RuntimeError('Forbidden by robots.txt')
     # не запрещено, вызываем функцию
     return urllib2.HTTPHandler.http_open(self, request)

class UserAgent(object):
    """
    Краулер.

    Именованные аргументы конструктора и значения по умолчанию:
    name -- имя ('Test/1.0')
    email -- адрес разработчика (пустая строка)
    headers -- словарь HTTP-заголовков (DEFAULT_HEADERS)
    """
    def __init__(self,
              agentname=DEFAULT_AGENTNAME,
              email=DEFAULT_EMAIL,
              new_headers={}):

     self.agentname = agentname
     self.email = email
     # для соединений будет использоваться OpenDirector,
     # лояльный к robots.txt.
     self.opener = urllib2.build_opener(
         RobotsHTTPHandler(self.agentname),
     )
     # переопределение заголовков по умолчанию
     headers = copy(DEFAULT_HEADERS)
     headers.update(new_headers)
     opener_headers = [ (k, v) for k, v in headers.iteritems() ]
     opener_headers.append(('User-Agent', self.agentname))
     # если email не задан, HTTP-заголовок 'From' не нужен
     if self.email:
         opener_headers.append(('From', self.email))

     self.opener.addheaders = opener_headers

    def open(self, url):
     """
     Возвращает file-like object, полученный с заданного адреса.
     В случае ошибки возвращает HTTPError, URLError или IOError.
     """
     return self.opener.open(url, None, TIMEOUT)