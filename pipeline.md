### Тэггинг корпуса

скрипт [./tagger/tagger.py](https://github.com/nevmenandr/thai-language/blob/master/tagger/tagger.py)

в `open_root` указываем путь к папке со скроуленнными текстами, они в [формате xml](https://github.com/nevmenandr/thai-language/blob/master/template.xml)

**! на момент 03.09.2016 скроулено 516 550 документов (176 073 973 токенов)**

в `write_root` указываем папку для сохранения теггированных текстов в [другом формате xml](https://github.com/nevmenandr/thai-language/blob/master/armenian_engine/examples_mapping/example_corpus.xml)

в `limit` указываем лимит в токенах

в файл `index.json` запишется максимальный индекс документа в корпусе

удаляем ненужные файлы и создаем директорию для результатов:

```
$ cd ~
$ rm -r text_tagged
$ mkdir text_tagged
```

запускаем скрипт:

```
$ python2 tagger.py
```

### Перевод текстов в формат для индексации армянским движком

скрипт [./armenian_engine/armenian_engine.py](https://github.com/nevmenandr/thai-language/blob/master/armenian_engine/armenian_engine.py)

в `open_root` указываем путь к папке с теггировнными текстами

в `write_root` указываем папку для сохранения текстов в [формате армянского движка](https://github.com/nevmenandr/thai-language/blob/master/armenian_engine/examples_mapping/example_corpus_file.prs)

удаляем ненужные файлы и создаем директорию для результатов:

```
$ rm -r [...]/ThaiCorpus/languages/thai/parsed_data
$ mkdir [...]/ThaiCorpus/languages/thai/parsed_data
```

запускаем скрипт:

```
$ cd ~
$ python2 armenian_engine.py
```

### Запуск индексатора

```
$ cd [...]/ThaiCorpus/indexator
$ python2 indexator.py
```
