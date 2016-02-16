import lxml.html, os, codecs

def readdict():
    arrwords=[]
    for root2, dirs, files in os.walk('thai_dict\\letters'):
        for file in files:
            f=codecs.open(os.path.join(root2, file), "r", "utf-8")
            f=f.read()
            root=lxml.html.fromstring(f)
            words=root.xpath('//table[@class="gridtable"]/tr')
            words=words[1:-1]
            for i in words:
                arrwords.append(i)
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
        self.pos=root.xpath('./td[@class="pos"]')[0].text_content()
        if self.thaiword!='NO':
            self.translit=root.xpath('./td')[1].text_content()
        else:
            self.translit='NO'
        try:
            self.translation=root.xpath('./td')[-1].text_content()
        except:
            self.translation='no'

def main():
    arrwords=readdict()
    final_arr=[]
    for i in arrwords:
        # print 'word: ', x.thaiword
        # print 'pos: ', x.pos
        # print 'translit: ', x.translit
        # print 'translation: ', x.translation
        # print '--------------------------------'
        if i not in final_arr:
            final_arr.append(Word(i))
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
