# cccTeam

##### Backend test version 2.0

----

**Nodejs**部分：`\couch`

用sh跑一个进程，通过读取本地文件夹的js文件，用`grunt-couch`在数据库上自动创建所需要的view

<img src="/Users/jenny/Library/Application Support/typora-user-images/image-20210509173321153.png" alt="image-20210509173321153" style="zoom:50%;"/>

Need to install `nodejs`

https://nodejs.org/zh-cn/

Run as `./exe.sh`

<img src="/Users/jenny/Library/Application Support/typora-user-images/image-20210509174758342.png" align='left' alt="image-20210509174758342" style="zoom:50%;" />

Test the JSON result by

http://admin:8185050@127.0.0.1:5984/twitter%2Fhist%2Fsydney%2Frelative/_design/scenario_1/_view/china_covid_stats?group=true

![image-20210509173449028](/Users/jenny/Library/Application Support/typora-user-images/image-20210509173449028.png)

---

**flask**部分：`\flask`

根据senario的需要，调取不同的view，结合aurin数据，整理好方便画图的格式，一起发给前端（在docker中跑）

http://0.0.0.0:9876/s1

<img src="/Users/jenny/Library/Application Support/typora-user-images/image-20210509174204543.png" align='left' alt="image-20210509174204543" style="zoom:50%;" />







