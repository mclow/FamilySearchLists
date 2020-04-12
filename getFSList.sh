#!/bin/bash

YOUAREHERE=$( dirname "${BASH_SOURCE[0]}" )

git pull
# get the data from familysearch.org; break it into lines, and save it into a file
./downloadFSJSON.py > today.json

# Compare with what we started with
./compareJSON.py FSList_base.json "today.json" 
