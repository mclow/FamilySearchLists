#!/bin/bash

YOUAREHERE=$( dirname "${BASH_SOURCE[0]}" )
echo $YOUAREHERE

TODAY=`date "+%Y%m%d"`

curl "https://familysearch.org/search/collectioninfo?summary=true&facets=OFF&offset=00&count=3000" | "$YOUAREHERE/format_collection.sh" > "FSList_$TODAY.json"

# curl "https://familysearch.org/search/collectioninfo?summary=true&facets=OFF&offset=00&count=3000" -o "FSList_$TODAY.json"

./compareJSON.py FSList_base.json "FSList_$TODAY.json" 
