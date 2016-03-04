import lxml.html, os, codecs

def readdict():
    arrwords=[]
    for root2, dirs, files in os.walk('thai_dict'):
        for file in files:
            print file
            f=codecs.open(os.path.join(root2, file), "r", "utf-8")
            f=f.read()
            root=lxml.html.fromstring(f)
            words=root.xpath('//table[@class="gridtable"]/tr')
            words=words[1:-1]
            for i in words:
                arrwords.append(i)
    print 'readdict finished'
    return arrwords

def deletedubs(arr):
    arr2=[]
    for i in arr:
        if i not in arr2:
            arr2.append(i)
    return arr2

class Word:
    def __init__(self, root=None):
        try:
            self.thaiword=root.xpath('./td[@class="th"]')[0].text_content()
        except:
            self.thaiword='NO'
        try:
            self.pos=root.xpath('./td[@class="pos"]')[0].text_content()
        except:
            pass
        if self.thaiword!='NO':
            self.translit=root.xpath('./td')[1].text_content()
        else:
            self.translit='NO'
        try:
            self.translation=root.xpath('./td')[-1].text_content()
        except:
            self.translation='NO'

def yaitron():
    import lxml.etree
    final_arr=[]
    dict=codecs.open('yaitron.xml', 'r', 'utf-8')
    dict=dict.read()
    root=lxml.etree.fromstring(dict)
    words=root.xpath('//entry')
    for word in words:
        i=Word()
        i.pos=word.xpath('/pos')[0].text
        i.thaiword=word.xpath('/headword')[0].text
        i.translit='NO'
        i.translation=word.xpath('/translation')[0].text
        final_arr.append(i)
    return final_arr

def writedict(arr):
    import json
    for word in arr:


def main():
    arrwords=readdict()
    final_arr=yaitron()
    for i in arrwords:
        if i not in final_arr:
            final_arr.append(Word(i))
    print 'starting deletedubs'
    final_arr=deletedubs(final_arr)
    for i in final_arr:
        if i.thaiword=="NO":
            i.thaiword=final_arr[final_arr.index(i)-1].thaiword
            i.translit=final_arr[final_arr.index(i)-1].translit
        print 'word: ', i.thaiword
        print 'pos: ', i.pos
        print 'translit: ', i.translit
        print 'translation: ', i.translation
        print '--------------------------------'
    return final_arr

main()
