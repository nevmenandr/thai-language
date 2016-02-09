import lxml.html, os

def readdict():
    arrwords=[]
    for root, dirs, files in os.walk('thai_dict/letters'):
        for file in files:
            f=file.read()
            root=lxml.html.fromstring(f)
            words=root.xpath('//table[@class="gridtable"]/tr')
            for i in words:
                arrwords.append(i)
    return arrwords

class Word:
    def __init__(self, root=None):
        self.thaiword=root.xpath('/td[@class="tz"]')[0].text
        self.pos=root.xpath('/td/span[@class="tt"]')[0].text
        self.translit=root.xpath('/td[@style="white-space:nowrap; text-align:right;"]')[0].text
        self.translation=root.xpath('/td[@style="vertical-align: top;"]')[0].text
