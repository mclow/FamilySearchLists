#!/bin/bash

# Format a collection list from ancestry.com.
# The data comes in as JSON, all on one line
# Remove the header, and break each "object" onto its' own line

sed -e "s/&quot;/\"/g" -e 's/{"recordCount":/\
  &/g' -e 's/]}"/\
]}/g' -e "s/data-jsondata=\"//" # -e "/^\./d"
