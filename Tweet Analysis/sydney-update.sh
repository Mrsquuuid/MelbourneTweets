#!bin/bash

cd '/Users/Ray/Dropbox (个人)/学习/2021SEM1/COMP90024/ASMT2/cccTeam/Tweet Analysis'

for year in 2019 2020; do
  for month in $(seq 1 12); do
    for day in $(seq 1 31); do
      echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
      echo "Downloading tweets in Sydney on: ${year}/${month}/${day}"
      curl "http://45.113.232.90/couchdbro/twitter/_design/twitter/_view/summary" -G --user 'readonly:ween7ighai9gahR6' -o 'temp/twitter.json' --data-urlencode start_key=[\"sydney\",$year,$month,$day] --data-urlencode end_key=[\"sydney\",$year,$month,$day] --data-urlencode 'reduce=false' --data-urlencode 'include_docs=true'
      echo "Processing tweets in Sydney on: ${year}/${month}/${day}"
      /opt/anaconda3/bin/python sydney-update.py $year $month $day
    done
  done
done
