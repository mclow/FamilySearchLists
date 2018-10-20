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

def imageString(idxCount, imgCount):
	idxStr = locale.format("%d", idxCount, grouping=True)
	imgStr = locale.format("%d", imgCount, grouping=True)
	if idxCount > 0 and imgCount > 0:
		retStr = "%s indexed records with %s record images" % (idxStr, imgStr)
	elif imgCount > 0:
		retStr = "Browse %s Images only, no index" % (imgStr)
	elif idxCount > 0:
		retStr = "Index only (%s records), no images" % (idxStr)
	else:
		retStr = "Index only, no images"
	return retStr

def imageStringWithDiffs(idxCount, imgCount, oldCount, oldImages):
	retStr = imageString(idxCount, imgCount)
	oldidxStr = locale.format("%d", oldCount, grouping=True)
	oldimgStr = locale.format("%d", oldImages, grouping=True)
	retStr += " (was %s records with %s images)" % (oldidxStr, oldimgStr)
	return retStr
	
def printCollection(coll, action):
	idxCnt = int(coll[u'count'])
	imgCnt = int(coll[u'count'])
	imgStr = imageString(idxCnt, imgCnt)
	print "%s\t(https://familysearch.org/search/collection/%s); %s, %s %s" % (coll[u'title'], coll[u'collectionId'], imgStr, action, coll[u'lastUpdate'])

def printCollectionWithDiffs(newColl, oldColl, action):
	idxCnt = int(newColl[u'count'])
	imgCnt = int(newColl[u'imageCount'])
	imgStr = imageStringWithDiffs(idxCnt, imgCnt, int(oldColl[u'count']), int(oldColl[u'imageCount']))
	print "%s\t(https://familysearch.org/search/collection/%s); %s, %s %s" % (newColl[u'title'], newColl[u'collectionId'], imgStr, action, newColl[u'lastUpdate'])


def printDict(d, label, action):
	print label
	for k in d.keys():
		printCollection(d[k], action)
#		print "%s\t(https://familysearch.org/search/collection/%s); xxx, Updated %s" % (d[k][u'title'], d[k][u'collectionId'], d[k][u'lastUpdate'])

def printDictWithDiffs(d, label, action):
	print label
	for k in d.keys():
		printCollectionWithDiffs(newEntries[k], oldEntries[k], action)
#		print "%s\t(https://familysearch.org/search/collection/%s); xxx, Updated %s" % (d[k][u'title'], d[k][u'collectionId'], d[k][u'lastUpdate'])

# {"collections":[{"collectionId":"1974186","title":"Argentina, Jujuy, Catholic Church Recor
locale.setlocale(locale.LC_ALL, 'en_US')
oldJSON = readJSON(sys.argv[1])[u"collections"]
newJSON = readJSON(sys.argv[2])[u"collections"]


# Given the two collections, generate four new collections.
# Unchanged, added, removed, updated

# key on collection ID for faster lookup
oldEntries = toDict(oldJSON)
newEntries = toDict(newJSON)

added = {}
removed = {}
updated = {}
moreImages = {}
fewerImages = {}
moreRecords = {}
fewerRecords = {}
unchanged = {}

# Find added, updated, and unchanged collections
for coll in newJSON:
	id = coll [u'collectionId']
	if not oldEntries.has_key(id):
		added[id] = coll
	else:
		oldColl = oldEntries[id]
		newColl = newEntries[id]
		if newColl[u'lastUpdateMillis'] < oldColl[u'lastUpdateMillis']:
			print "## Collection ", id, " has regressed (datewise)!"

		if   newColl[u'lastUpdateMillis'] > oldColl[u'lastUpdateMillis']:
			updated[id] = coll
		elif newColl[u'imageCount']       > oldColl[u'imageCount']:
			moreImages[id] = coll
		elif newColl[u'imageCount']       < oldColl[u'imageCount']:
			fewerImages[id] = coll
		elif newColl[u'count']       > oldColl[u'count']:
			moreRecords[id] = coll
		elif newColl[u'count']       < oldColl[u'count']:
			fewerRecords[id] = coll
		else:
#			assert(newColl[u'count'] == oldEntries[id][u'count'])
			unchanged[id] = coll

# Find added collections
for coll in oldJSON:
	id = coll [u'collectionId']
	if not newEntries.has_key(id):
		removed[id] = coll

printDict(removed, "--- Collections Deleted ---", "DELETED")
print
printDict(added,   "--- Collections Added   ---", "ADDED")
print
printDictWithDiffs(updated, "--- Collections Updated ---", "Updated")
print
printDictWithDiffs(moreImages, "--- Collections with new images ---", "")
print
printDictWithDiffs(fewerImages, "--- Collections with images removed ---", "")
print
printDictWithDiffs(moreRecords, "--- Collections with new records ---", "")
print
printDictWithDiffs(fewerRecords, "--- Collections with records removed ---", "")
print

# print len(oldJSON), len (newJSON), len(unchanged)
