#!/bin/bash
# Need to install nodejs before running this script
# https://nodejs.org/zh-cn/
sudo npm install -g grunt-cli
sudo npm install grunt --save-dev
sudo npm install grunt-cli --save-dev
sudo npm install grunt-couch --save-dev
grunt couch-compile
grunt couch-push