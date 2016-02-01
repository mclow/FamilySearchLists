#!/bin/bash

YOUAREHERE=$( dirname "${BASH_SOURCE[0]}" )
echo $YOUAREHERE

TODAY=`date "+%Y%m%d"`

# get the data from familysearch.org; break it into lines, and save it into a file
curl "http://www.ancestry.com/cs/recent-collections" | grep "data-jsondata" | "$YOUAREHERE/format_ancestry.sh" > "AncestryList_$TODAY.json"

# Compare with what we started with
# ./compareJSON.py AncestryList_base.json "AncestryList_$TODAY.json" 
