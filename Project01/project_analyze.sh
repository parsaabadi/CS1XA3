#!/bin/bash

rm -f ./todo.log
IFS=$'\n'
for f in `find . -type f | grep -v analysis.sh`; do
  for line in `cat $f`; do
    echo "$line #TODO" >> ./todo.log
  done
done

FILES=".html:HTML
.js:JavaScript
.css:CSS
.py:Python
.hs:Haskell
.sh:Bash"

for line in $FILES; do
  ext=`echo $line | cut -d: -f1`
  name=`echo $line | cut -d: -f2`
  count=`find . -type f | grep "$ext" | wc -l`
  echo "$name: $count"
done
