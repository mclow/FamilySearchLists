#!/usr/bin/env python3
# switched from /usr/bin/python for working SSL support
# 
import sys, os, re
import json
import codecs
import locale
from lxml import html
import requests

## Before 15-Apr-2022, FamilySearch embedded the list of collections
## In the web page as a JSONstring.
# page = requests.get("https://www.familysearch.org/search/collection/list/")
# tree = html.fromstring(page.content)
# scripts = tree.xpath('//script')
# findJS = re.compile('let collectionList = ([^\n]+);\n')
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

## As of 19-Nov-2022, FamilySearch rejects requests that don't contain a user-agent
## header. 

def getCollectionList ():
# 	user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0'}
# 	url = "https://www.familysearch.org/search/webservice/collectionListData"
# 	page = requests.get(url, headers = user_agent)
# 	collections = json.loads(page.content)
	with open("collectionListData.json") as json_data:
		collections = json.load(json_data)
	return collections ["collectionList"]


cList = getCollectionList ()
print(json.dumps(cList, sort_keys=True, indent=2))

# Manual work
# Load up https://www.familysearch.org/en/search/collection/list?count=All
# Break into developer tools (cmd-option-C)
# Look at sources ; filter by XDR; find the one as https://www.familysearch.org/search/orchestration/collectionListData
# save the contents as "collectionListData.json"
