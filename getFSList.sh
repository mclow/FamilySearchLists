#!/bin/bash

TODAY=`date "+%Y%m%d"`

curl "https://familysearch.org/search/collectioninfo?summary=true&facets=OFF&offset=00&count=3000" | sed -e 's/{"collectionId":/\
  &/g' -e 's/],/\
],/g' > "FSList_$TODAY.json"

# curl "https://familysearch.org/search/collectioninfo?summary=true&facets=OFF&offset=00&count=3000" -o "FSList_$TODAY.json"

./compareJSON.py FSList_base.json "FSList_$TODAY.json" 
