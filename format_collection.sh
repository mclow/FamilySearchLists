#!/bin/bash

# Format a collection list from familysearch.org.
# The data comes in as JSON, all on one line
# Break each "object" onto its' own line

sed -e 's/{"collectionId":/\
  &/g' -e 's/],/\
&/g'
