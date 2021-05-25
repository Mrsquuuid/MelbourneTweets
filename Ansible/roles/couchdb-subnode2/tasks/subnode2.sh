#!/bin/bash

echo "== Set variables =="
declare -x -a nodes=(172.17.0.4 172.17.0.3 172.17.0.2)
export masternode=`echo ${nodes} | cut -f1 -d' '`
declare -x -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export size=${#nodes[@]}
export user='admin'
export pass='admin'
export VERSION='3.1.1'
export cookie='a192aeb9904e6590849337933b000c99'

echo "== Start the containers =="
docker create\
      --name couchdb172.26.130.150\
      -p 5984:5984 -p 4369:4369 -p 9100-9200:9100-9200\
      --env COUCHDB_USER=${user}\
      --env COUCHDB_PASSWORD=${pass}\
      --env COUCHDB_SECRET=${cookie}\
      --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@172.26.130.150\""\
      ibmcom/couchdb3:${VERSION}
sleep 3
docker start couchdb172.26.130.150
sleep 3

curl -XPOST "http://admin:admin@172.26.133.54:5984/_cluster_setup" \
      --header "Content-Type: application/json"\
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
             \"username\": \"admin\", \"password\":\"admin\", \"port\": \"5984\",\
             \"remote_node\": \"172.26.130.150\", \"node_count\": \"3\",\
             \"remote_current_user\":\"admin\", \"remote_current_password\":\"admin\"}"
sleep 3

curl -X POST -H "Content-Type: application/json" http://admin:admin@172.26.130.150:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "node_count":"3"}'
sleep 3
