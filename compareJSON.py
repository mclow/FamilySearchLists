#!/usr/bin/env python3
# 
# A script for comparing two collection lists from familysearch.org
# The lists are JSON files, where the entry 'collections' points to 
# an array of dictionaries, with keys like:
# 	'collectionId'		: The unique identifier for this collection
# 	'title'				: The Title for this collection (should be unique, but not required to be)
# 	'lastUpdate'		: the last date that this collection was updated
# 	'lastUpdatdeMillis'	: the last update time of this collection (used to tell if the colleciton has changed)
# 
# We build a pair of dictionaries from the two JSON structures, 
# where each collection is an entry, and the collectonId is the key.
# Then we use those two dictionaries to find collections that have been added/removed/updated.

# Future refinement: See http://stackoverflow.com/questions/4527942/comparing-two-dictionaries-in-python
# especially "Daniel"'s answer

import sys, os
import json
import codecs
import locale
import datetime

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
	idxStr = locale.format_string("%d", idxCount, grouping=True)
	imgStr = locale.format_string("%d", imgCount, grouping=True)
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
	oldidxStr = locale.format_string("%d", oldCount, grouping=True)
	oldimgStr = locale.format_string("%d", oldImages, grouping=True)
	retStr += " (was %s records with %s images)" % (oldidxStr, oldimgStr)
	return retStr
	
def printCollection(aColl, action, withTimeStamp):
	
	idxCnt = int(aColl[u'recordCount'])
	imgCnt = int(aColl[u'imageCount'])
	imgStr = imageString(idxCnt, imgCnt)
	if withTimeStamp:
		ts = datetime.datetime.fromtimestamp(int(aColl[u'lastUpdatedMillis'])//1000)
		stStr = ts.strftime('%d-%b-%Y')
		print("%s\t(https://familysearch.org/search/collection/%s); %s, %s %s" % (aColl[u'title'], aColl[u'collectionId'], imgStr, action, stStr))
	else:
		print("%s\t(https://familysearch.org/search/collection/%s); %s, %s"    % (aColl[u'title'], aColl[u'collectionId'], imgStr, action))

def printCollectionWithDiffs(newColl, oldColl, action):
	ts = datetime.datetime.fromtimestamp(int(newColl[u'lastUpdatedMillis'])//1000)
	stStr = ts.strftime('%d-%b-%Y')

	idxCnt = int(newColl[u'recordCount'])
	imgCnt = int(newColl[u'imageCount'])
	imgStr = imageStringWithDiffs(idxCnt, imgCnt, int(oldColl[u'recordCount']), int(oldColl[u'imageCount']))
	print("%s\t(https://familysearch.org/search/collection/%s); %s, %s %s" % (newColl[u'title'], newColl[u'collectionId'], imgStr, action, stStr))


def printDict(d, label, action, withTimeStamp = True):
	print("%s" % label)
	for k in d.keys():
		printCollection(d[k], action, withTimeStamp)
#		print "%s\t(https://familysearch.org/search/collection/%s); xxx, Updated %s" % (d[k][u'title'], d[k][u'collectionId'], d[k][u'lastUpdate'])

def printDictWithDiffs(d, label, action):
	print("%s" % label)
	for k in d.keys():
		printCollectionWithDiffs(newEntries[k], oldEntries[k], action)
#		print "%s\t(https://familysearch.org/search/collection/%s); xxx, Updated %s" % (d[k][u'title'], d[k][u'collectionId'], d[k][u'lastUpdate'])

# {"collections":[{"collectionId":"1974186","title":"Argentina, Jujuy, Catholic Church Recor
locale.setlocale(locale.LC_ALL, 'en_US')

# From https://stackoverflow.com/questions/4545661/unicodedecodeerror-when-redirecting-to-file
# sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 
# From https://stackoverflow.com/questions/4374455/how-to-set-sys-stdout-encoding-in-python-3
sys.stdout.reconfigure(encoding='utf-8')

oldJSON = readJSON(sys.argv[1])# [u"collections"]
newJSON = readJSON(sys.argv[2])# [u"collections"]


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

# Sanity checking
for coll in newJSON:
	id = coll [u'collectionId']
# 	print id
	if not u'lastUpdatedMillis' in coll:
		print("Collection %s has no update time" % id)
	if not u'imageCount' in coll:
		print("Collection %s has no image count" % id)
	if not u'recordCount' in coll:
		print("Collection %s has no record count" % id)

# Find added, updated, and unchanged collections
for coll in newJSON:
	id = coll [u'collectionId']
	if not id in oldEntries:
		added[id] = coll
	else:
		oldColl = oldEntries[id]
		newColl = newEntries[id]
		if newColl[u'lastUpdatedMillis'] < oldColl[u'lastUpdatedMillis']:
			print("## Collection ", id, " has regressed (datewise)!")

		if   newColl[u'lastUpdatedMillis'] > oldColl[u'lastUpdatedMillis']:
			updated[id] = coll
		elif newColl[u'imageCount']       > oldColl[u'imageCount']:
			moreImages[id] = coll
		elif newColl[u'imageCount']       < oldColl[u'imageCount']:
			fewerImages[id] = coll
		elif newColl[u'recordCount']       > oldColl[u'recordCount']:
			moreRecords[id] = coll
		elif newColl[u'recordCount']       < oldColl[u'recordCount']:
			fewerRecords[id] = coll
		else:
#			assert(newColl[u'count'] == oldEntries[id][u'count'])
			unchanged[id] = coll

# Find added collections
for coll in oldJSON:
	id = coll [u'collectionId']
	if not id in newEntries:
		removed[id] = coll

print("## There are %5d entries in the old list" % len(oldEntries.keys()))
print("## There are %5d entries in the new list" % len(newEntries.keys()))
print()
print("## There are %5d removed entries" % len(removed.keys()))
print("## There are %5d added entries" % len(added.keys()))
print("## There are %5d updated entries" % len(updated.keys()))
print("## There are %5d entries with more images" % len(moreImages.keys()))
print("## There are %5d entries with less images" % len(fewerImages.keys()))
print("## There are %5d entries with more records" % len(moreRecords.keys()))
print("## There are %5d entries with less records" % len(fewerRecords.keys()))
print("## There are %5d unchanged entries" % len(unchanged.keys()))


printDict(removed, "--- Collections Deleted ---", "DELETED", False)
print()
printDict(added,   "--- Collections Added   ---", "ADDED")
print()
printDictWithDiffs(updated, "--- Collections Updated ---", "UPDATED")
print()
printDictWithDiffs(moreImages, "--- Collections with new images ---", "last updated")
print()
printDictWithDiffs(fewerImages, "--- Collections with images removed ---", "last updated")
print()
printDictWithDiffs(moreRecords, "--- Collections with new records ---", "last updated")
print()
printDictWithDiffs(fewerRecords, "--- Collections with records removed ---", "last updated")
print()

# printDict(unchanged,   "--- Collections Unchanged   ---", "UNCHANGED")

# print len(oldJSON), len (newJSON), len(unchanged)
