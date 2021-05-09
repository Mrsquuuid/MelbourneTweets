# cccTeam

##### Backend test version 2.0

----

**Nodejs**部分：`\couch`

用sh跑一个进程，通过读取本地文件夹的js文件，用`grunt-couch`在数据库上自动创建所需要的view

<img src="https://github.com/Mrsquuuid/cccTeam/blob/27db70362a11e25d598a429c2c1a6488e4e155e7/image/1.png" height="30%" width="30%"/>


Need to install `nodejs`

https://nodejs.org/zh-cn/

Run as `./exe.sh`

<img src="https://github.com/Mrsquuuid/cccTeam/blob/27db70362a11e25d598a429c2c1a6488e4e155e7/image/2.png" height="40%" width="40%"/>


Test the JSON result by

http://admin:8185050@127.0.0.1:5984/twitter%2Fhist%2Fsydney%2Frelative/_design/scenario_1/_view/china_covid_stats?group=true

<img src="https://github.com/Mrsquuuid/cccTeam/blob/27db70362a11e25d598a429c2c1a6488e4e155e7/image/3.png" height="80%" width="80%">

---

**flask**部分：`\flask`

根据senario的需要，调取不同的view，结合aurin数据，整理好方便画图的格式，一起发给前端（在docker中跑）

http://0.0.0.0:9876/s1

<img src="https://github.com/Mrsquuuid/cccTeam/blob/27db70362a11e25d598a429c2c1a6488e4e155e7/image/4.png" height="20%" width="20%">







