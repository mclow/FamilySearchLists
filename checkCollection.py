#!/usr/bin/python
# 
# A script for checking a collection list from familysearch.org
# The lists are JSON files, where the entry 'collections' points to 
# an array of dictionaries, with keys like:
# 	'collectionId'		: The unique identifier for this collection
# 	'title'				: The Title for this collection (should be unique, but not required to be)
# 
# Things to check:
#  * No duplicate collectionIds
#  * No duplicate collection titles

import sys, os
import json

def readJSON(filename):
	with open(filename) as json_data:
		d = json.load(json_data)
		json_data.close()
	return d

# {"collections":[{"collectionId":"1974186","title":"Argentina, Jujuy, Catholic Church Recor
j1 = readJSON(sys.argv[1])[u"collections"]

# Given the two collections, generate four new collections.
# Unchanged, added, removed, updated

ids = set()
titles = set()

for item in j1:
	colid = item [u'collectionId']
	title = item [u'title']
	if colid in ids:
		print "## Duplicate collection ID: %s" % colid
	if title in titles:
		print "## Duplicate collection title: %s" % title
	ids.add(colid)
	titles.add(title)

print len(j1), len(ids), len(titles)
