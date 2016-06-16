# -*- coding:utf-8 -*-

import codecs, os, lxml.etree, json


def trainingset():
    arr = [[]]
    for root2, dirs, files in os.walk('thaipoem.com'):
        for file in files:
            f = codecs.open(os.path.join(root2, file), "r", "utf-8")
            exemel = f.read()
            f.close()
            root = lxml.etree.fromstring(exemel)[1]
            words = root.xpath('./w')
            n = 0
            while n < len(words):
                try:
                    lex = words[n].xpath('./ana')[0]
                    if lex.get('lex') != '' and lex.get('pos') != '':
                        arr[-1].append((lex.get('lex'), lex.get('pos')))
                    else:
                        arr.append([])
                    n += 1
                except:
                    n += 1
            arr.append([])
    labelled_sequences = []
    for x in arr:
        if len(x) > 1:
            labelled_sequences.append(x)
    tag_set=set()
    symbols = set()
    for i in labelled_sequences:
        for n in i:
            tag_set.add(n[1])
            symbols.add(n[0])
    return labelled_sequences, tag_set, symbols


def trainer():
    import nltk
    import dill
    labelled_sequences, tag_set, symbols = trainingset()
    trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)
    hmm = trainer.train_supervised(labelled_sequences)
    hmm.test(labelled_sequences[:1000], verbose=False)
    with open('my_tagger.dill', 'wb') as f:
        dill.dump(hmm, f)
    f.close()

trainer()
