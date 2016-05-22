#!/bin/bash
mkdir -p maps
mv maps_* maps/
for i in *.jpg
do
name=$(echo $i | cut -f 1 -d '.')
composite -geometry +490+490 "maps/maps_$name.jpg" "$i" "cap_$i"
text=`cat "km_$name.txt"`
convert "cap_$i" -gravity northwest -pointsize 20 -stroke black -strokewidth 4 -annotate 0 "${text} km"      -stroke white -strokewidth 1 -fill white -annotate 0 "${text} km" "caption_$i"
echo $name
done
