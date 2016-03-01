# -*- coding:utf-8 -*-

import glob
import re
import codecs
from subprocess import call

# python3!

""" Программка сначала вызывает wget (сейчас эта функция дезактивирована),
затем очищает от метаразметки полученные html-файлы.
Wget должен лежать в одной папке с программой.
Скачать его можно здесь:
http://wget.addictivecode.org/FrequentlyAskedQuestions?action = show&redirect = Faq#download
"""
name = "http://www.thairath.co.th/ent/novel"


def download_texts(name):
    """Call wget an download texts from the site """
    call(['wget','-r', '-np', '-nc', name])
    
# download_texts(name)

n = 0

for files in glob.glob(r"/home/gree-gorey/Py/thai-language/crawlers/www.thairath.co.th/ent/novel/kuwunlunpanrak/*"):
    n += 1
    f = codecs.open(files, 'r', 'utf-8')
    # name = re.findall(r"\\([^\\]*)", str(files))
    # name = str(n) + '_' + str(name[-1]) + '.txt'
    name = str(files) + '.txt'
    outfile = codecs.open(name, 'w', 'utf-8')
    unit = f.read().split('\t')
    for elem in unit:
        elem = re.findall(r'<p>.*',elem)
        if len(elem)>0:
            for one in elem:
                one = re.sub('(<p>|</p>)','',one)
                one = re.sub('<br />','\n', one)
                one = re.sub('&ldquo;','"',one)
                one = re.sub('&rdquo;','"',one)
                outfile.write(str(one) + u'\n')
    f.close()
    outfile.close()

print("Yes we can!")
