#!/bin/bash
if [ $1 ]; then
	cat $1  | uniq -c | perl -ple 's/^\s*(\d+)\s+(.+)/$2\t$1/'
fi
