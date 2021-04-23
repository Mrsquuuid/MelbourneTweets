#Precautions for initializing Ubuntu:

Specific process:

1. 修改environment配置文件：
~~~~
vim /etc/environment
~~~~
加入以下配置
~~~~
HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/
HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/
http_proxy=http://wwwproxy.unimelb.edu.au:8000/
https_proxy=http://wwwproxy.unimelb.edu.au:8000/
no_proxy=localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.unimelb.edu.au,.cloud.unimelb.edu.au
~~~~
注：如果使用vi命令出现bug，使用如下语句：
~~~~
sudo su
echo "set nocp" >> ~/.vimrc
source ~/.vimrc
~~~~
2.更新apt-get
~~~~
sudo apt-get update
~~~~
更新完装点必要的软件就可以了：
~~~~
sudo apt install docker.io
sudo apt install vim
...
~~~~
3.如果想要正常拉取镜像，还需要进一步配置。
reference：https://docs.docker.com/config/daemon/systemd/#httphttps-proxy
~~~~
sudo mkdir -p /etc/systemd/system/docker.service.d
touch http-proxy.conf
vim http-proxy.conf
~~~~
在该文件里写入：
~~~~
[Service]
Environment="HTTP_PROXY=http://wwwproxy.unimelb.edu.au:8000/"
Environment="HTTPS_PROXY=http://wwwproxy.unimelb.edu.au:8000/"
Environment="http_proxy=http://wwwproxy.unimelb.edu.au:8000/"
Environment="https_proxy=http://wwwproxy.unimelb.edu.au:8000/"
Environment="no_proxy=localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.org.au,.storage.unimelb.edu.au,.cloud.unimelb.edu.au“
~~~~
检查下引号格式
4.配置改完刷新并重启docker
~~~~
 sudo systemctl daemon-reload
 sudo systemctl restart docker
~~~~
5.验证配置,确保environment的值被写进去。
~~~~
sudo systemctl show --property=Environment docker
~~~~
6.测试
~~~~
docker run hello-world
~~~~

#Tips for installing couchdb:
1. Don't forget to modify the profile(local.ini)!
2. If you want to start a CouchDB service with docker, https://blog.csdn.net/qq_43378019/article/details/116031996 has some useful info.
