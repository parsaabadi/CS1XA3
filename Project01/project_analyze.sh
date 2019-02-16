##updated version
#!/bin/bash

rm ./todo.log
grep -rin "#TODO" . | grep -v todo.log > /tmp/todo.log
mv /tmp/todo.log ./

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
