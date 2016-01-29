#!/usr/bin/python

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
# for i in range(0,5):
# 	print j1[i]['collectionId'], '\t', j1[i]['lastUpdate'], '\t', j1[i]['title']

# Given the two collections, generate four new collections.
# Unchanged, added, removed, updated

# key on collection ID for faster lookup
d1 = toDict(j1)
d2 = toDict(j2)

added = {}
removed = {}
updated = {}
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
		else:
			unchanged[id] = coll

# Find added collections
for coll in j2:
	id = coll [u'collectionId']
	if not d1.has_key(id):
		added[id] = coll

printDict(removed, "--- Collections Deleted ---")
printDict(added,   "--- Collections Added   ---")
printDict(updated, "--- Collections Updated ---")
# print len(j1), len (j2), len(unchanged)
