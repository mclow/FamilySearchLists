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

## Before 15-Apr-2022, FamilySearch embedded the list of collections
## In the web page as a JSONstring.
# page = requests.get("https://www.familysearch.org/search/collection/list/")
# tree = html.fromstring(page.content)
# scripts = tree.xpath('//script')
# 
# 
# for s in scripts:
# 	if s.text != None:
# 		m = findJS.search(s.text)
# 		if m != None:
# 			j = json.loads(m[1])
# 			print(json.dumps(j, indent=2))
# 			break

## As of 15-Apr-2022, FamilySearch made the list of collections a seperate
## page that is loaded by the web page.
page = requests.get("https://www.familysearch.org/search/webservice/collectionListData")
collections = json.loads(page.content)
cList = collections ["collectionList"]
print(json.dumps(cList, indent=2))