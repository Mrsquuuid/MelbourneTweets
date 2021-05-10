echo "=============checkout Backend code from github==================="
cd ~
sudo apt-get install git
git init
git clone http://qiyiz-uni:Zhangqiyi261725@github.com/Mrsquuuid/cccTeam
git checkout qiyiz-mrc
cd couch

echo "=============Done==================="
echo "  "

echo "=============Deploy nodejs and Grunt environment==================="
cd ~
wget https://nodejs.org/dist/v10.15.3/node-v10.15.3-linux-x64.tar.xz
tar xf node-v10.15.3-linux-x64.tar.xz

cd node-v10.15.3-linux-x64/
./bin/node -v

sudo ln -s ~/node-v10.15.3-linux-x64/bin/node /usr/bin
sudo ln -s ~/node-v10.15.3-linux-x64/bin/npm /usr/bin

# check nodejs and npm ready
echo "nodejs version"
sudo node -v
echo "npm version"
sudo npm -v

{
	cd ~
	sudo npm install -g grunt-cli
	PATH=$PATH:$HOME/bin:/home/ubuntu/node-v10.15.3-linux-x64/bin/

	cd /home/ubuntu/couch

	sudo npm install grunt --save-dev
	sudo npm install grunt-cli --save-dev
	sudo npm install grunt-couch --save-dev
} &> /dev/null

echo "=============Done==================="
echo "  "


echo "=============Compile and push map-reduce views==================="
grunt couch-compile
grunt couch-push


echo "======generating views==================="
curl http://admin:admin@172.17.0.4:5984/twitter/_design/scenario_1/_view/china_covid_stats?group=true
curl http://admin:admin@172.17.0.4:5984/twitter/_design/scenario_1/_view/china_stats?group=true
curl http://admin:admin@172.17.0.4:5984/twitter/_design/scenario_1/_view/china_vulgar_stats?group=true
echo "=============Done==================="


