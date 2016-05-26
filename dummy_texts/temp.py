# -*- coding: utf-8 -*-

import os
import codecs
from lxml import etree
import pythai

__author__ = 'gree-gorey'


dictionary = {
  "อย่างคุยโม้โอ้อวด": {
    "1": [
      "pompously",
      [
        "adverb"
      ],
      ""
    ]
  },
  "การเชื่อมโยงความคิดสองอย่างเข้าด้วยกัน ต้องมีปัจจัยสนับสนุนที่ดีพอ": {
    "1": [
      "To connect two ideas together, there must be a sufficiently reasonable bridging concept.",
      [
        "example sentence"
      ],
      "gaanM cheuuamF yo:hngM khwaamM khitH saawngR yaangL khaoF duayF ganM dtawngF meeM bpatL jaiM saL napL saL noonR theeF deeM phaawM"
    ]
  },
  "เสียกำลังใจ (คำไม่เป็นทางการ)": {
    "1": [
      "have one's tail down down",
      [
        "idiom"
      ],
      ""
    ]
  },
  "ปล่อยเวลาให้เสียไปโดยเปล่าประโยชน์ (คำไม่เป็นทางการ)": {
    "1": [
      "goof around",
      [
        "PHRV"
      ],
      ""
    ]
  },
  "ผอ ": {
    "1": [
      "[pronunciation of the 28th letter of the Thai alphabet]",
      [
        ""
      ],
      "phaawR"
    ]
  },
  "ความสะเทือนใจ": {
    "1": [
      "depression",
      [
        "noun"
      ],
      ""
    ],
    "2": [
      "depression",
      [
        "noun"
      ],
      ""
    ]
  },
  "เฉพาะกิจ": {
    "1": [
      "[is] special; special purpose",
      [
        "adjective"
      ],
      "chaL phawH gitL"
    ],
    "2": [
      "specific",
      [
        "adjective"
      ],
      ""
    ]
  },
  "พระองค์เจ้า": {
    "1": [
      "the king's son born by a lesser concubine",
      [
        "noun",
        "proper noun",
        "person",
        "phrase",
        "formal"
      ],
      "phraH ohngM jaoF"
    ]
  },
  "ปิติทุบแก้วเสียหรือ": {
    "1": [
      "Did Piti break the glass?",
      [
        "example sentence"
      ],
      "bpiL dtiL thoopH gaaeoF siiaR reuuR"
    ]
  },
  "ต้อยต่ำ": {
    "1": [
      "humble",
      [
        "adjective"
      ],
      ""
    ],
    "2": [
      "[is] humble; lowly; inferior",
      [
        "adjective"
      ],
      "dtaawyF dtamL"
    ]
  },
  "โต๊ะหรือแท่นที่มีสามขา": {
    "1": [
      "tripod",
      [
        "noun"
      ],
      ""
    ]
  },
  "การปีนเขา": {
    "1": [
      "mountaineering",
      [
        "noun"
      ],
      ""
    ]
  },
  "ซึ่งกระตือรือร้นที่จะสนับสนุนในเรื่องใดเรื่องหนึ่งและต้องการให้คนอื่นเชื่อเหมือนกับตัวเอง": {
    "1": [
      "evangelic",
      [
        "adjective"
      ],
      ""
    ],
    "2": [
      "evangelical",
      [
        "adjective"
      ],
      ""
    ]
  },
  "ซึ่งทำให้ตรง": {
    "1": [
      "unbendable",
      [
        "adjective"
      ],
      ""
    ]
  },
  "เครื่องมือที่ทำให้เกิดเปลวไฟ เพื่อใช้เป็นสัญญาณ": {
    "1": [
      "flare",
      [
        "noun"
      ],
      ""
    ]
  },
  "แมลงเม่าบินเข้ากองไฟ": {
    "1": [
      "Flying termites fly into the fire. — To act on impulse or recklessly. — Like a moth to a flame",
      [
        "example sentence",
        "idiom"
      ],
      "maH laaengM maoF binM khaoF gaawngM faiM"
    ]
  },
  "เปลี่ยนจากรู้สึกสุขเป็นเศร้า": {
    "1": [
      "laugh on",
      [
        "PHRV"
      ],
      ""
    ]
  },
  "เผ่นพรวด": {
    "1": [
      "leap suddenly",
      [
        "verb"
      ],
      ""
    ]
  },
  u"เบียดเสียด": {
    "1": [
      "crowd",
      [
        "verb",
        "intransitive"
      ],
      ""
    ],
    "2": [
      "to crowd; flock; throng; congregate; swarm; mass",
      [
        ""
      ],
      "biiatL siiatL"
    ],
    "3": [
      "crowd",
      [
        "verb"
      ],
      ""
    ],
    "4": [
      "crowd",
      [
        "verb",
        "transitive"
      ],
      ""
    ],
    "5": [
      "squash",
      [
        "verb",
        "intransitive"
      ],
      ""
    ],
    "6": [
      "squash",
      [
        "verb",
        "transitive"
      ],
      ""
    ]
  }
}


def read_xml(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            open_name = path + filename
            print filename
            with codecs.open(open_name, u'r', u'utf-8') as f:
                tree = etree.parse(f)
            return tree, filename


def pos(string):
    tokens = pythai.split(string)
    return tokens


def sentence_iterator(text):
    sentences = [[u'', True]]
    previous_is_thai = True
    for char in text:
        if 3585 <= ord(char) <= 3675:
            if not previous_is_thai:
                sentences.append([u'', True])
            sentences[-1][0] += char
            previous_is_thai = True
        else:
            if previous_is_thai:
                sentences.append([u'', False])
            sentences[-1][0] += char
            previous_is_thai = False
    for sentence, is_thai in sentences:
        if sentence:
            yield sentence, is_thai


def main():
    for ana_number in dictionary[u'เบียดเสียด']:
        ana = dictionary[u'เบียดเสียด'][ana_number]
        print ana
    # tree, filename = read_xml(u'./corpus_from_tagged/')
    # se = tree.xpath('//meta/link')
    # print filename
    # print se[0].text
    # print pos(u'¯°.¸♥♥¯° ศรรกรา ¯°.¸♥♥¯°what°¯♥♥¸.°´¯')
    # print ord(u'๛')
    # text = u'¯°.¸♥♥¯°ศรรกราหน้าทะเล้น°¯♥♥¸.°´¯'
    # for sentence, is_thai in sentence_iterator(text):
    #     print sentence, is_thai

    # a = [[0, 1], [2, 3]]
    # for one, two in a:
    #     print one, two

if __name__ == '__main__':
    main()
