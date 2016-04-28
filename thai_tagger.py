# -*- coding: utf-8 -*-

import codecs, os, shutil, json, re
import pythai
#DICT = u"/home/new_words/thai/dict/dict_fil.json"
DICT = u"/home/new_words/thai/dict/test_dict_2.json"
def main():
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
        #print i
        for j in i[-1]:
            tag_file(i[0] + u"/" + j, dictionary)
            
def tag_file(path, dictionary): ##DONE
    new_file = codecs.open(path, "r", "utf-8")
    is_text = False
    res = u""
    for i in new_file:
        #print type(i)
        #if is_text:
        #    res += tag_text(i, dictionary)
        #else:
        #    res += i
	is_flag = True
        if u"<text>" in i and not u"</text>" in i:
            #print i
    	    is_text = True
	    is_flag = False
        elif u"</text>" in i:
            is_text = False
	if is_text:
	    res += tag_text(i, dictionary)
	else:
	    res += i
            #text = new_file.read()
    new_file.close()
    #text = text_clear(text)
    #texts, text = text_clear(text)
    #print texts
    #tag_texts = []
    #for i in texts:
        #tag_texts.append(tag_text(i, dictionary))
    #parts = text.split(u"@#")
    #i = 0
    
    #for i in parts:
        #res += i
        #if i < len(tag_texts):
            #res += tag_texts[i]
            #i += 1
    new_file = codecs.open(path, "w", "utf-8")
    new_file.write(res)
    new_file.close()
    #os.remove(path)
    
    
def tag_text(text, dictionary): ##hmmm...
    #print u"###", text
    result = [u"<body>"]
    sents = text.split()
    for i in sents:
        result.append(u"<se>")
        for j in pythai.split(i):
            result.append(tag_word(j, dictionary))
        result.append(u"</se>")
    result.append(u"</body>")
    return create_xml(result)

def tag_word(word, dictionary): #!!!
    if u"<text>" in word:
	return u"<text>"
    if u"</text>" in word:
	return u"</text>"
    res = u"<w>"
    if word in dictionary:
        for i in dictionary[word]:
            flag = dictionary[word][i]
            res += u"<ana lex=" + u'"' + word + u'"' + u" pos=" 
	    for k in flag[1]:
		res += u'"' + k + u'",'
	    res = res[:-1] 
	    res += u" trans=" + u'"' + flag[0] + u'"' + u" translit=" + u'"' + flag[2] +'"></ana>'
    res = res + word + u"</w>"
    #print res
    #print "\n\n"
    return res

def create_xml(result):
    return u"\r\n".join(result)


def text_clear(text):
    get_text = re.compile(u"<text>.*</text>")
    #texts = get_text.findall(text)
    #print texts
    text = get_text.sub(u"@#", text)
    #for i in xrange(len(texts)):
        #texts[i] = texts[i].replace(u"<text>", u"")
        #texts[i] = texts[i].replace(u"</text>", u"")
    #return texts, text
    return text

#=============================================================
def read_data (path):
    data_file = codecs.open(path, 'r', 'utf-8')
    data = json.load(data_file)
    data_file.close()
    return data       

def write_data (path, data):
    json_data = json.dumps(data, ensure_ascii=False, indent=1)  
    json_file = codecs.open (path, 'w', 'utf-8')
    json_file.write (json_data)
    json_file.close()

if __name__ == '__main__':
    main()

#a = codecs.open("149071.xml", "r", "utf-8")
#b = a.read()
#c = text_clear(b)
#print c
