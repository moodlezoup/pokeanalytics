#!/bin/bash

months="2014-11 2014-12 2015-01 2015-02 2015-03 2015-04 2015-05 2015-06 2015-07 2015-08 2015-09 2015-10 2015-11 2015-12 2016-01 2016-02 2016-03 2016-04 2016-05 2016-06 2016-07 2016-08 2016-09 2016-10 2016-11"
files="ru-0.json ru-1500.json ru-1630.json ru-1760.json"
for month in $months
do
    mkdir "data/$month"
    cd "data/$month"
    for file in $files
    do
        wget "http://www.smogon.com/stats/$month/chaos/$file"
    done
    cd "../.."
done
