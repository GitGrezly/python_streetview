#!/bin/bash
mkdir -p maps
mv maps_* maps/
for i in *.jpg
do
name=$(echo $i | cut -f 1 -d '.')
composite -geometry +490+490 "maps/maps_$name.jpg" "$i" "caption_$i"
echo $name
done
