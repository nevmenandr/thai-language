# -*- coding: utf-8 -*-

import codecs, os, shutil, json
import pythai
DICT = u"/home/new_words/thai/dict/dict.json"

def main():
    global DICT
    path_load = get_path() 
    #path_load = u"c:\\test" #вставка 
    dictionary = read_data(DICT)
    
    path_save = copy_repository(path_load)
    tag_repository (path_save, dictionary)

def get_path():
    path = "/home/new_words/thai/test_tagger" # raw_input(u"Path: ")
    return path

#=========================================================

def copy_repository(path_load): ##DONE
    path_save = path_load + u"_tagged"
    index = 1
    changed = False
    if os.path.exists(path_save):
        changed = True
        while os.path.exists(path_save + " (" + unicode(index) + ")"):
            index += 1
    if changed:
        path_save = path_save + " (" + unicode(index) + ")"
    shutil.copytree(path_load, path_save)
        
    return path_save

def tag_repository(repository, dictionary): ##DONE
    for i in os.walk(repository):
        print i
        for j in i[-1]:
            tag_file(i[0] + u"/" + j, dictionary)
            
def tag_file(path, dictionary): ##DONE
    new_file = codecs.open(path, "r", "utf-8")
    text = new_file.read()
    new_file.close()
    text = text.clear(text)###
    text = tag_text(text, dictionary)

    new_file = codecs.open(path+u".xml", "w", "utf-8")
    new_file.write(text)
    new_file.close()
    os.remove(path)
    
    
def tag_text(text, dictionary): ##hmmm...
    result = [u"<body>"]
    sents = text.split()
    for i in sents:
        result.append(u"<se>")
        for j in pythai.split(i):
            result.append(tag_word(j, dictionary))
        result.append(u"</se>")
    result.append(u"</body>") 
    return create_csv(result)

def tag_word(word, dictionary): #!!!
    res = u"<w>"
    if word in dictionary:
        for i in dictionary[word]:
            flag = dictionary[word][i]
            res += u"<ana lex=" + u'"' + word + u'"' + u" gr=" + u'"' + flag[1]+ u'"' + u" trans=" + u'"' + flag[0] + u'"></ana>'
    res = res + word + u"</w>"
    return res

def create_csv(result):
    return u"\r\n".join(result)


def text_clear(text):
    get_text = re.compile(u"<text>.*?</text>")
    get_tags = re.compile(u"</?text>?")
    texts = get_text.findall(text)
    print texts
    for i in xrange(len(texts)):
        texts[i] = get_tags.sub(texts[i], u"")
    return u" ".join(texts)

#=============================================================
def read_data (path):
    data_file = codecs.open(path, 'r', 'utf-8')
    data = json.load(data_file)
    data_file.close()
    return data       

def write_data (path, data):
    json_data = json.dumps(data, ensure_ascii=False, indent=1)  
    json_file = codecs.open (path, 'w', 'cp1251')
    json_file.write (json_data)
    json_file.close()

if __name__ == '__main__':
    main()
