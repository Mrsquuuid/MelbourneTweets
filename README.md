## 1. Precautions for initializing Ubuntu:

Specific process:

1. Modify the environment configuration file：
~~~~
vim /etc/environment
~~~~
Add the following configuration
~~~~
HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/
HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/
http_proxy=http://wwwproxy.unimelb.edu.au:8000/
https_proxy=http://wwwproxy.unimelb.edu.au:8000/
no_proxy=localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.unimelb.edu.au,.cloud.unimelb.edu.au
~~~~
Note: if there is a bug using VI command, use the following statement
~~~~
sudo su
echo "set nocp" >> ~/.vimrc
source ~/.vimrc
~~~~
2.Update apt-get
~~~~
sudo apt-get update
~~~~
Install some software:
~~~~
sudo apt install docker.io
sudo apt install vim
...
~~~~
3.If you want to pull the image normally, you need further configuration.
reference：https://docs.docker.com/config/daemon/systemd/#httphttps-proxy
~~~~
sudo mkdir -p /etc/systemd/system/docker.service.d
cd /etc/systemd/system/docker.service.d
touch http-proxy.conf
vim http-proxy.conf
~~~~
Write these in the file:
~~~~
[Service]
Environment="HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/"
Environment="HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/"
Environment="http_proxy=http://wwwproxy.unimelb.edu.au:8000/"
Environment="https_proxy=http://wwwproxy.unimelb.edu.au:8000/"
Environment="no_proxy=localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.unimelb.edu.au,.cloud.unimelb.edu.au“
~~~~
4.Refresh and restart docker after configuration change
~~~~
 sudo systemctl daemon-reload
 sudo systemctl restart docker
~~~~
5.Verify the configuration and make sure that the value of environment is written in.
~~~~
sudo systemctl show --property=Environment docker
~~~~
6.Test
~~~~
docker run hello-world
docker run -d -p 5984:5984 -e COUCHDB_USER="admin" -e COUCHDB_PASSWORD=123456 ibmcom/couchdb3
~~~~


## 2. When creating a CouchDB cluster, what should I do if a specific IP refuses to connect:
Input at terminal:
~~~~
unset http_proxy
unset https_proxy
~~~~

## 3. Tips for installing couchdb:
1. Don't forget to modify the profile(local.ini)!
2. If you want to start a CouchDB service with docker, https://blog.csdn.net/qq_43378019/article/details/116031996 has some useful info.

## 4. Tips for deploying flask project by gunicorn:
There are many ways, but pip install is likely to report an error. At this time, you need to declare the proxy in the dockerfile, otherwise you cannot download the image. https://stackoverflow.com/questions/30992717/proxy-awareness-with-pip For example:
~~~~
pip install --proxy=http://wwwproxy.unimelb.edu.au:8000/ {sth. you want to download}
~~~~
This project: 172.26.133.50:80
