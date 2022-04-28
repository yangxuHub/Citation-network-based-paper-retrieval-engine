#!/bin/bash
length=

if [[ -n $1 ]]
then
    length=$1
fi
for I in `seq 0 $length`;do
  mongoimport --db IR --collection citations --file ./all_final/part_$I.jsonl && echo "part $I imported"
done
echo "citation data imported"
