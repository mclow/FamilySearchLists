#!/bin/bash

YOUAREHERE=$( dirname "${BASH_SOURCE[0]}" )
echo $YOUAREHERE

TODAY=`date "+%Y%m%d"`

# get the data from familysearch.org; break it into lines, and save it into a file
curl "https://familysearch.org/search/collectioninfo?summary=true&facets=OFF&offset=00&count=3000" | "$YOUAREHERE/format_collection.sh" > "FSList_$TODAY.json"

# Compare with what we started with
./compareJSON.py FSList_base.json "FSList_$TODAY.json" 
