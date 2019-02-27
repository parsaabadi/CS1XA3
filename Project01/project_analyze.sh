#!/bin/bash

FILETYPES=".html:HTML
.js:JavaScript
.css:CSS
.py:Python
.hs:Haskell
.sh:Bash"

function analysis {
rm -f ./parsa.log
grep -rin "#PARSA" . | grep -v parsa.log > /tmp/parsa.log
mv /tmp/parsa.log ./

  rm -f ./todo.log
  IFS=$'\n'
  files=`find . -type f | egrep "\.(html|js|css|py|hs|sh)$" | grep -v "\.git" | grep -v analysis.sh`
  for f in $files; do
    for line in `cat $f`; do
      echo "$line #TODO" >> ./todo.log
    done
  done

  for line in $FILETYPES; do
    ext=`echo $line | cut -d: -f1`
    name=`echo $line | cut -d: -f2`
    count=`find . -type f | grep "$ext" | wc -l`
    echo "$name: $count"
  done
}

function compile {
  echo "" > compile_fail.log
  for f in `find . -type f -name "*.py"`; do
    python -m py_compile $f >> compile_fail.log 2>&1
  done
  for f in `find . -type f -name "*.hs"`; do
    ghc $f >> compile_fail.log 2>&1
  done
}

function untracked {
  files=`git ls-files . --exclude-standard --others | grep "\.tmp"`
  for f in $files; do
    echo "removing file: $f"
    rm $f
  done
}

if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Please provide --analysis, --compile, or --untracked"
else
  if [ "$1" == "--analysis" ]
    then
      analysis
  elif [ "$1" == "--compile" ]
    then
      compile
  elif [ "$1" == "--untracked" ]
    then
      untracked
  else
    echo "No arguments supplied. Please provide --analysis, --compile, or --untracked"
  fi
fi
