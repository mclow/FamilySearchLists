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

def printDict(d, label):
	print label
	titles = []
	for k in d.keys():
		titles.append(d[k][u'title'])
	for t in sorted(titles):
#	for t in titles:
		print t

# {"collections":[{"collectionId":"1974186","title":"Argentina, Jujuy, Catholic Church Recor
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
			assert(d2[id][u'count'] == d1[id][u'count'])
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
