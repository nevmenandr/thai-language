# -*- coding: utf-8 -*-

from polyglot.text import Text
from polyglot.transliteration import Transliterator

__author__ = 'gree-gorey'

"""
Это если хочешь транслитить предложение
"""

blob = u'รัตนกศรีสยาม เรืองนามจากแผ่นดินถึงถิ่นสวรรค์'
text = Text(blob)

for x in text.transliterate(target_language="en"):
    print(x)

"""
А так можно транслитить по одному слову. Больше слова не транслитит(
"""

transliterator = Transliterator(source_lang="th", target_lang="en")

print transliterator.transliterate(u'เรืองนาม')
