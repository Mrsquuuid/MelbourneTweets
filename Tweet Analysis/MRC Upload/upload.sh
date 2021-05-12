cd /home/ubuntu/couch-db/couch-db-split
unset http_proxy
unset https_proxy
for db in $(ls); do
  echo "processing database: ${db}"
  curl -X PUT "http://172.17.0.4:5984/${db}" --user "admin:admin"
  cd $db
    for file in $(ls); do 
      echo "Uploading: ${file} @ ${db}"
      curl -X POST "http://172.17.0.4:5984/${db}/_bulk_docs" --user "admin:admin" -H "Content-Type: application/json" --data @$file
    done
  cd ../
done