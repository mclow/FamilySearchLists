#!/usr/bin/env python3
# switched from /usr/bin/python for working SSL support
# 
import sys, os, re
import json
import codecs
import locale
from lxml import html
import requests

findJS = re.compile('let collectionList = ([^\n]+);\n')

# From https://stackoverflow.com/questions/4374455/how-to-set-sys-stdout-encoding-in-python-3
# sys.stdout.reconfigure(encoding='utf-8')

page = requests.get("https://www.familysearch.org/search/collection/list/")
tree = html.fromstring(page.content)
scripts = tree.xpath('//script')


for s in scripts:
	if s.text != None:
		m = findJS.search(s.text)
		if m != None:
#			print (s.text[0:70])
#			print (m[1][:70])
#			print (m[1][-70:])
			j = json.loads(m[1])
			print(json.dumps(j, indent=2))
			break
