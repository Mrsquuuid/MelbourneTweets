#!/bin/bash


declare -x -a nodes=(172.17.0.4 172.17.0.3 172.17.0.2)
export masternode=`echo ${nodes} | cut -f1 -d' '`
declare -x -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export size=${#nodes[@]}
export user='admin'
export pass='admin'
export VERSION='3.1.1'
export cookie='a192aeb9904e6590849337933b000c99'

export size=${#nodes[@]}

echo "== Start the container =="
docker create\
      --name couchdb172.26.133.54\
      -p 5984:5984 -p 4369:4369 -p 9100-9200:9100-9200\
      --env COUCHDB_USER=${user}\
      --env COUCHDB_PASSWORD=${pass}\
      --env COUCHDB_SECRET=${cookie}\
      --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@172.26.133.54\""\
      ibmcom/couchdb3:${VERSION}
sleep 3

docker start couchdb172.26.133.54








#echo "== Start the container =="
#docker run -d -p 5984:5984 -p 4369:4369 -p 9100-9200:9100-9200 --name=mastercouchdb couchdb:3.1.1
#sleep 3
#
#docker exec mastercouchdb bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
#docker exec mastercouchdb bash -c "echo \"-name couchdb@${masternode}\" >> /opt/couchdb/etc/vm.args"
#
#docker restart mastercouchdb
#sleep 15
#
#echo "== Enable cluster setup =="
#for (( i=0; i<${size}; i++ )); do
#    curl -X PUT "http://${nodes[${i}]}:5984/_node/_local/_config/admins/${user}" --data "\"${password}\""
#    sleep 3
#    curl -X PUT "http://${user}:${password}@${nodes[${i}]}:5984/_node/couchdb@${nodes[${i}]}/_config/chttpd/bind_address" --data '"0.0.0.0"'
#    sleep 2
#done
#
#echo "== Add nodes to cluster =="
#for (( i=0; i<${size}; i++ )); do
#    if [ "${nodes[${i}]}" != "${masternode}" ]; then
#        curl -X POST -H 'Content-Type: application/json' http://${user}:${password}@${masternode}:5984/_cluster_setup \
#            -d "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\", \"username\": \"${user}\", \"password\":\"${password}\", \"port\": 5984, \"node_count\": \"${size}\", \
#            \"remote_node\": \"${nodes[${i}]}\", \"remote_current_user\": \"${user}\", \"remote_current_password\": \"${password}\"}"
#        curl -X POST -H 'Content-Type: application/json' http://${user}:${password}@${masternode}:5984/_cluster_setup \
#            -d "{\"action\": \"add_node\", \"host\":\"${nodes[${i}]}\", \"port\": 5984, \"username\": \"${user}\", \"password\":\"${password}\"}"
#    fi
#done
#
#echo "== Finish cluster =="
#curl -X POST -H "Content-Type: application/json" "http://${user}:${password}@${masternode}:5984/_cluster_setup" -d '{"action": "finish_cluster"}'
