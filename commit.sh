#!/bin/bash

if [ $# != 1 ]; then
	echo "Must pass a commit message"
	exit 1
fi

mv today.json FSList_base.json
git commit FSList_base.json -m "$1"
git push
