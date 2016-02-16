import lxml.html, os

def readdict():
    arrwords=[]
    for root, dirs, files in os.walk('thai_dict/letters'):
        for file in files:
            f=file.read()
            root=lxml.html.fromstring(f)
            words=root.xpath('//table[@class="gridtable"]/tr')
            for i in words:
                arrwords.append(i)import lxml.html, os, codecs

def readdict():
    arrwords=[]
    for root2, dirs, files in os.walk('thai_dict\\letters'):
        for file in files:
            f=codecs.open(os.path.join(root2, file), "r", "utf-8")
            f=f.read()
            root=lxml.html.fromstring(f)
            words=root.xpath('//table[6]/tr')
            print words[0].text_content()
            for i in words:
                arrwords.append(i)
    return arrwords

class Word:
    def __init__(self, root=None):
        try:
            self.thaiword=root.xpath('/td[@class="th"]')[0].text
        except:
            self.thaiword='no'
        try:
            self.pos=root.xpath('/td[@class=pos]')[0].text
        except:
            self.pos='no'
        try:
            self.translit=root.xpath('/td')[0][1].text
        except:
            self.translit='no'
        try:
            self.translation=root.xpath('/td')[0][-1].text
        except:
            self.translation='no'

def main():
    arrwords=readdict()
    final_arr=[]
    for i in arrwords:
        x=Word(i)
        print x.thaiword
        final_arr.append(x)
    return final_arr

main()

    return arrwords

class Word:
    def __init__(self, root=None):
        self.thaiword=root.xpath('/td[@class="tz"]')[0].text
        self.pos=root.xpath('/td/span[@class="tt"]')[0].text
        self.translit=root.xpath('/td[@style="white-space:nowrap; text-align:right;"]')[0].text
        self.translation=root.xpath('/td[@style="vertical-align: top;"]')[0].text
