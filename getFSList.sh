#!/bin/bash

YOUAREHERE=$( dirname "${BASH_SOURCE[0]}" )

# get the data from familysearch.org; break it into lines, and save it into a file
curl "https://familysearch.org/search/collectioninfo?summary=true&facets=OFF&offset=00&count=3000" | "$YOUAREHERE/format_collection.sh" > "today.json"

# Compare with what we started with
./compareJSON.py FSList_base.json "today.json" 
