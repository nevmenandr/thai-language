# -*- coding: utf-8 -*-
import urllib2
import re
import codecs
import HTMLParser
import os

hPrs = HTMLParser.HTMLParser()

visited = []
to_be_visited = []
