#!/usr/bin/python
# 
# A script for comparing two collection lists from familysearch.org
# The lists are JSON files, where the entry 'collections' points to 
# an array of dictionaries, with keys like:
# 	'collectionId'		: The unique identifier for this collection
# 	'title'				: The Title for this collection (should be unique, but not required to be)
# 	'lastUpdate'		: the last date that this collection was updated
# 	'lastUpdateMillis'	: the last update time of this collection (used to tell if the colleciton has changed)
# 
# We build a pair of dictionaries from the two JSON structures, 
# where each collection is an entry, and the collectonId is the key.
# Then we use those two dictionaries to find collections that have been added/removed/updated.

# Future refinement: See http://stackoverflow.com/questions/4527942/comparing-two-dictionaries-in-python
# especially "Daniel"'s answer

import sys, os
import json
import locale

def readJSON(filename):
	with open(filename) as json_data:
		d = json.load(json_data)
		json_data.close()
	return d

def toDict(collection):
	d = {}
	for item in collection:
		d [ item [u'collectionId']] = item
	return d

def printCollection(coll):
	imgCnt = int(coll[u'count'])
	if imgCnt > 0:
		imgStr = "%s indexed records with record images" % locale.format("%d", imgCnt, grouping=True)
	else:
		imgStr = "Browse Images only, no index"
	print "%s\t(https://familysearch.org/search/collection/%s); %s, Updated %s" % (coll[u'title'], coll[u'collectionId'], imgStr, coll[u'lastUpdate'])


def printDict(d, label):
	print label
	for k in d.keys():
		printCollection(d[k])
#		print "%s\t(https://familysearch.org/search/collection/%s); xxx, Updated %s" % (d[k][u'title'], d[k][u'collectionId'], d[k][u'lastUpdate'])


# {"collections":[{"collectionId":"1974186","title":"Argentina, Jujuy, Catholic Church Recor
locale.setlocale(locale.LC_ALL, 'en_US')
j1 = readJSON(sys.argv[1])[u"collections"]
j2 = readJSON(sys.argv[2])[u"collections"]


# Given the two collections, generate four new collections.
# Unchanged, added, removed, updated

# key on collection ID for faster lookup
d1 = toDict(j1)
d2 = toDict(j2)

added = {}
removed = {}
updated = {}
moreImages = {}
unchanged = {}

# Find deleted, updated, and unchanged collections
for coll in j1:
	id = coll [u'collectionId']
	if not d2.has_key(id):
		removed[id] = coll
	else:
		assert(d2[id][u'lastUpdateMillis'] >= d1[id][u'lastUpdateMillis'])
		if d2[id][u'lastUpdateMillis'] > d1[id][u'lastUpdateMillis']:
			updated[id] = coll
		elif d2[id][u'imageCount'] > d1[id][u'imageCount']:
			moreImages[id] = coll
		else:
#			assert(d2[id][u'count'] == d1[id][u'count'])
			unchanged[id] = coll

# Find added collections
for coll in j2:
	id = coll [u'collectionId']
	if not d1.has_key(id):
		added[id] = coll

printDict(removed, "--- Collections Deleted ---")
printDict(added,   "--- Collections Added   ---")
printDict(updated, "--- Collections Updated ---")
printDict(moreImages, "--- Collections with new images ---")

# print len(j1), len (j2), len(unchanged)
