#!/bin/bash

# apply the instances, render the templates
. ./unimelb-comp90024-group-80-openrc.sh; ansible-playbook apply-instance.yml
# . ./unimelb-comp90024-group-80-openrc.sh; ansible-playbook --ask-become-pass apply-instance.yml

# install docker on the remote servers
ansible-playbook -i inventory.ini -u ubuntu docker-configuration.yml

# reset the enviroment of the remote servers
# ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group80 -v environment-reset.yml

# setup couchdb cluster on database servers
ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group80 couchdb-cluster-setup.yml

# setup the web server and load the data
ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group80 background-configuration.yml
