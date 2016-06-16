# -*- coding: utf-8 -*-

import codecs, os, shutil, re, json

def write_data (path, data):
    json_data = json.dumps(data, ensure_ascii=False, indent=1)  
    json_file = codecs.open (path, 'w', 'utf-8')
    json_file.write (json_data)
    json_file.close()
def read_data (path):
    data_file = codecs.open(path, 'r', 'utf-8')
    data = json.load(data_file)
    data_file.close()
    return data     

def main (path, rules_path):
    rules = read_data(rules_path)
    for text, fname in read_xml(path):
        tagged_text = tag_file(text, rules)

def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = root + "\\" + filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                text = f.read()
            yield text, filename

def tag_file (text, rules):
    s_text = text.split("<se>")
    for ss_text in s_text[1:]:
        parts = ss_text.split("</se>")
        if parts:
            res = tag_sent(parts[0], rules)
            #print ">> ", parts[0], "\n"

def tag_sent(sent, rules): ##Тут дописывать
    #print "==================================="
    sent = re.sub("<w>", "", sent)
    words = sent.split("</w>")
    tagged_words = []
    for i in words:
        res = tag_word(i)
        tagged_words.append(res)
    flag = 0
    for i in rules:
        flag += 1
        res = compare(i, tagged_words)
        if res:
            for j in i:
                print j[u"gr"]
                #tagged_words[res[0][0]:res[0][1]], "\n", i, "\n==============\n"
        #if res and len(i) != 2:
            #print res, ": ", len(i)
            #for j in res:
                
            
         #   print flag, ": ", res #, "\n", i#, "\n", i
##        for j in tagged_words:
##            for 
##            if (i[0]["lex"] == ) and () and () and ():
##                pass

def compare (rule, words):
    length = len(rule)
    result = []
    cut = 0
    while cut < len(words):
        part = words[cut : cut + length]
        #print len(part)
        if cut + length == len(words):
            is_end = True
            
        if len(part) == length:
            add = 0
            for i in range(length):
                cut_correct = 0
                
                is_lex = False
                is_pos = False
                correct = False
                #print part
                for omo in part[i]:
                    if len(omo) > 1:
                        for j in rule[i][u"lex"]:
                            if j.strip() == omo[0].strip().strip(u'"'):
                                is_lex = True
                        for j in rule[i][u"pos"]:
                            if j in omo[1]:
                                is_pos = True
                if is_pos and is_lex:
                    correct = True
                    #print True
                if correct:
                    add += 1
            if add == length:
                result.append([cut, cut + length - 1])
                cut += (length - 1)

        cut += 1
    return result    #for var in omo:
                 #   if len(var) > 3:
                        
        
def tag_word(word):
    summ = []
    parts = word.split("<ana ")
    for i in parts:
        res = re.findall('".*?"', i)
        summ.append(res)
    return summ
    
main("c:\\test", "rules_test1.json")

##a = [
##[{u"leх":u"กำลัง",u"pos":None,u"end_sentence":False,u"gr":u"prs"},{u"lex":None,u"pos":[u"transitive",u"intransitive",u"auxiliary verb"],u"end_sentence":False,u"gr":u"prs"}],
##[{u"leх":None,u"pos":u"transitive/intransitive/auxiliary verb",u"end_sentence":False,u"gr":u"prs"},{u"leх":u"อยู่",u"pos":None,u"end_sentence":False,u"gr":u"prs"}],
##[{u"leх":u"จะ",u"pos":None,u"end_sentence":False,u"gr":u"fut"},{u"lex":None,u"pos":u"transitive/intransitive/auxiliary verb",u"end_sentence":False,u"gr":u"fut"}],
##[{u"leх":u"ได้",u"pos":None,u"end_sentence":False,u"gr":u"pst"},{u"lex":None,u"pos":u"transitive/intransitive/auxiliary verb",u"end_sentence":False,u"gr":u"pst"}],
##[{u"leх":u"มา",u"pos":None,u"end_sentence":False,u"gr":u"pst"},{u"leх":None,u"pos":None,u"end_sentence":True,u"gr":None}],
##[{u"leх":u"ไม่",u"pos":None,u"end_sentence":False,u"gr":u"neg"},{u"leх":None,u"pos":u"transitive/intransitive/auxiliary verb",u"end_sentence":False,u"gr":None}],
##[{u"leх":u"กำลัง",u"pos":None,u"end_sentence":False,u"gr":u"inten"},{u"leх":u"จะ",u"pos":None,u"end_sentence":False,u"gr":u"inten"},{u"leх":None,u"pos":u"transitive/intransitive/auxiliary verb",u"end_sentence":False,u"gr":u"inten"}],
##[{u"leх":None,u"pos":u"noun/proper noun/pronoun",u"end_sentence":False,u"gr":None},{u"leх":None,u"pos":u"adjective",u"end_sentence":False,u"gr":u"cmpr"},{u"leх":u"กว่า",u"pos":None,u"end_sentence":False,u"gr":u"cmpr"},{u"leх":None,u"pos":u"noun/proper noun/pronoun",u"end_sentence":False,u"gr":None}],
##[{u"leх":None,u"pos":u"noun/proper noun/pronoun",u"end_sentence":False,u"gr":None},{u"leх":None,u"pos":u"adjective",u"end_sentence":False,u"gr":u"sup"},{u"leх":u"ที่สุด",u"pos":None,u"end_sentence":False,u"gr":u"sup"}],
##[{u"leх":u"พวก",u"pos":None,u"end_sentence":False,u"gr":u"pl"},{u"leх":None,u"pos":u"noun/proper noun/pronoun",u"end_sentence":False,u"gr":u"pl"}]
##]
##write_data("d:\\test\\rules_test.json", a)
