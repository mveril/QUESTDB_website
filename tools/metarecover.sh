#!/bin/bash
files=$(git status -s | grep " M "  | cut -c4- | grep 'static/data/')
for file in $files; do
  show="$(git --no-pager show HEAD~1:$file)"
  IFS=$'\n' lines=($show)
  for (( i=0; i<=5; i++ )) ;do  
    line=${lines[i]}
    sed -i "$((i+1))s|^.*$|$line|" $file
  done
done