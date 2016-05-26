import codecs, os, shutil, re
from lxml import etree
rules_path = ""

def open_xml(path):
    root = etree.parse(path)
    nodes = root.xpath("//text()")
    for node in nodes:
        print node#.tag,node.keys(),node.values()
