#!/bin/bash

source ../lib/bookratios.shlib
url="$(config_get baseurl)"
period="$(config_get period)"

IFS=',' read -r -a depths <<< "$(config_get depths)"

for element in "${depths[@]}"
do
    newurl="${url/BOOKPCT/$element}"
    finalurl="${newurl/PERIOD/$period}"
    echo "$finalurl"
    wget --output-document=../data/bitcoinity_data_${element}_pct.csv $finalurl
done


