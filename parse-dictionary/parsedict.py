import lxml.html, os, codecs


class Word:
    def __init__(self, root=None):
        try:
            self.thaiword = root.xpath('./td[@class="th"]')[0].text_content()
        except:
            self.thaiword = 'NO'
        try:
            self.pos = root.xpath('./td[@class="pos"]')[0].text_content()
        except:
            pass
        if self.thaiword != 'NO':
            self.translit = root.xpath('./td')[1].text_content()
        else:
            self.translit = 'NO'
        try:
            self.translation = root.xpath('./td')[-1].text_content()
        except:
            self.translation = 'NO'


def readdict():
    arrwords = []
    for root2, dirs, files in os.walk('thai_dict'):
        for file in files:
            print file
            f = codecs.open(os.path.join(root2, file), "r", "utf-8")
            f = f.read()
            root = lxml.html.fromstring(f)
            words = root.xpath('//table[@class="gridtable"]/tr')
            words = words[1:-1]
            for i in words:
                arrwords.append(Word(i))
    print 'readdict finished'
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
    print 'dict read'
    root = lxml.etree.fromstring(dict)
    words = root.xpath("//entry[@lang='tha']")
    for word in words:
        i = Word()
        i.pos = word.xpath('./pos')[0].text
        i.thaiword = word.xpath('./headword')[0].text
        i.translit = 'NO'
        i.translation = word.xpath('./translation')[0].text
        final_arr.append(i)
        print i.translation + ' appended'
        i = None
    words = root.xpath("//entry[@lang='eng']")
    for word in words:
        i = Word()
        try:
            i.pos = word.xpath('./pos')[0].text
        except:
            i.pos = "pos is missing"
        i.translation = word.xpath('./headword')[0].text
        i.translit = 'NO'
        i.thaiword = word.xpath('./translation')[0].text
        final_arr.append(i)
        print i.translation + ' appended'
        i = None
    print 'yaitron finished'
    return final_arr


def writedict(arr):
    import json
    f = codecs.open('slovar.json', 'w', 'utf-8')
    d = {}
    print 'starting with dict'
    for i in arr:
        d[i.thaiword]={}
    print 'i made an empty dict'
    for i in d:
        count=1
        for n in arr:
            d[n.thaiword][count]=[n.translation, n.pos, n.translit]
            count+=1
            print n.thaiword, d[n.thaiword]
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.close()


def main():
    arrwords = readdict()
    final_arr = yaitron()
    final_arr.extend(arrwords)
    print 'next'
    # for i in arrwords:
    #     if i not in final_arr:
    #         final_arr.append(Word(i))
    #         print Word(i).translation+' finally appended'
    final_arr = set(final_arr)
    final_arr = list(final_arr)
    writedict(final_arr)
    for i in final_arr:
        if i.thaiword == "NO":
            i.thaiword = final_arr[final_arr.index(i) - 1].thaiword
            i.translit = final_arr[final_arr.index(i) - 1].translit
        print 'word: ', i.thaiword
        print 'pos: ', i.pos
        print 'translit: ', i.translit
        print 'translation: ', i.translation
        print '--------------------------------'
    return final_arr


main()
