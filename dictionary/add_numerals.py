#Add numerals

import codecs
from collections import Counter
import json
import re

f = codecs.open('new_slovar.json', 'r', 'utf-8')
text = f.read()
f.close()
slovar = json.loads(text)

f = codecs.open('numerals.json', 'r', 'utf-8')
text = f.read()
f.close
numerals = json.loads(text)

full_slovar = {key: value for (key, value) in (slovar.items() + numerals.items())}
new_slovar = json.dumps(full_slovar, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
f = codecs.open(u'new_slovar.json', 'w', 'utf-8')
f.write(new_slovar)
f.close()
