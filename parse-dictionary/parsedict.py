# -*- coding: utf-8 -*-
import lxml.html, os, codecs


class Word:
    def __init__(self, root=None):
        try:
            self.thaiword = root.xpath('./td[@class="th"]')[0].text_content()
        except:
            self.thaiword = 'NO'
        try:
            self.pos = root.xpath('./td[@class="pos"]')[0].text_content().split(', ')
        except:
            self.pos = [""]
        if self.thaiword != 'NO':
            self.translit = root.xpath('./td')[1].text_content()
        else:
            self.translit = 'NO'
        try:
            self.translation = root.xpath('./td')[-1].text_content()
        except:
            self.translation = 'NO'

    def __gt__(self, other):
        return self.thaiword > other.thaiword

    def __lt__(self, other):
        return self.thaiword < other.thaiword

    def posmerge(self):
        changedict = {
            'ADJ': 'adjective',
            'adj': 'adjective',
            'N': 'noun',
            '์N': 'noun',
            '์์N': 'noun',
            'ืN': 'noun',
            'V': 'verb',
            '์V': 'verb',
            'VI': 'verb, intransitive',
            'VT': 'verb, transitive',
            'ADV': 'adverb',
            'AVD': 'adverb',
            'PRON': 'pronoun',
            'AUX': 'auxiliary verb',
            'IDM': 'idiom',
            'ABBR': 'abbreviation',
            'INT': 'interjection',
            'CONJ': 'conjunction',
            'CLAS': 'classifier',
            'PREP': 'preposition',
            'PREF': 'prefix',
            'ADV   V': 'adverb, verb'
        }
        for i in self.pos:
            if i in changedict:
                if i == 'VI' or i == 'VT' or i=='ADV   V':
                    self.pos.extend(changedict[i].split(', '))
                else:
                    self.pos.append(changedict[i])
                self.pos.remove(i)
        return self


def readdict():
    arrwords = []
    for root2, dirs, files in os.walk('thai_dict'):
        for file in files:
            f = codecs.open(os.path.join(root2, file), "r", "utf-8")
            f = f.read()
            root = lxml.html.fromstring(f)
            words = root.xpath('//table[@class="gridtable"]/tr')
            words = words[1:-1]
            for i in words:
                arrwords.append(Word(i))
    return arrwords


def deletedubs(arr):
    arr2 = []
    for i in arr:
        if i not in arr2:
            arr2.append(i)
    return arr2


def yaitron():
    import lxml.etree
    final_arr = []
    dict = codecs.open('yaitron.xml', 'r', 'utf-8')
    dict = dict.read()
    root = lxml.etree.fromstring(dict)
    words = root.xpath("//entry[@lang='tha']")
    for word in words:
        i = Word()
        i.pos = [word.xpath('./pos')[0].text]
        i.thaiword = word.xpath('./headword')[0].text
        i.translit = 'NO'
        i.translation = word.xpath('./translation')[0].text
        final_arr.append(i)
        i = None
    words = root.xpath("//entry[@lang='eng']")
    for word in words:
        i = Word()
        try:
            i.pos = word.xpath('./pos')[0].text.split(', ')
        except:
            i.pos = [""]
        i.translation = word.xpath('./headword')[0].text
        i.translit = ''
        i.thaiword = word.xpath('./translation')[0].text
        i = i.posmerge()
        final_arr.append(i)
        i = None
    return final_arr


def writedict(arr):
    import json
    f = codecs.open('slovar5.json', 'w', 'utf-8')
    d = {}  # финальный словарь
    subd = []  # служебный массив
    subd2 = {}  # служебный словарь
    arr.sort()  # сортировка по тайским словам
    for i in arr:
        subd2[i] = [i.translation, i.pos,
                    i.translit]  # делаем служебный словарь: каждому объекту ставим в соответствие перевод, часть речи и транслит
        subd.append(
            [i.translation, i.pos, i.translit])  # делаем служебный массив значений, отсортированный по тайским словам
    keyss = [i.thaiword for i in arr]
    keyss = list(set(keyss))
    keyss.sort()  # отсортированный массив тайских слов
    count2 = 0
    for i in keyss:
        c = 1
        d[i] = {}
        for n in arr[count2::]:
            if i == n.thaiword:
                d[i][c] = [n.translation, n.pos, n.translit]
                c += 1
            else:
                count2 = arr.index(n)
                break
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.close()


def main():
    arrwords = readdict()
    final_arr = yaitron()
    final_arr.extend(arrwords)
    for i in final_arr:
        if i.thaiword == "NO":
            i.thaiword = final_arr[final_arr.index(i) - 1].thaiword
            i.translit = final_arr[final_arr.index(i) - 1].translit
    final_arr = set(final_arr)
    final_arr = list(final_arr)
    final_arr.sort()
    writedict(final_arr)
    return final_arr


main()
