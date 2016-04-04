#!/bin/bash
mkdir new/
images=0

for i in $(ls maps*.jpg); do
    let images=images+1
done


i=1
factor=0
while [ $factor -lt $images ]; do
    new_name=$((images-factor))  
    printf $new_name' '
    mv $i.jpg new/$new_name.jpg
    mv maps_$i.jpg new/maps_$new_name.jpg
    let factor=factor+1
    let i=i+1
done
echo ''
