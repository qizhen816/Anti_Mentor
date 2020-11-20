# Anti_Mentor
This is an honorable instrunction of automatically warning yourself when working fish in lab.

#如何在办公室反监控小米摄像头快乐摸鱼  
主要思路是模拟浏览器登录路由器管理网页→进入监控流量上传下载的子网页→找到摄像头ID→监控上传流量→发现异常报警，打开学术页面

*需要满足的条件*：TP-Link路由器，否则需要自行修改页面逻辑

**我爬虫太菜了，不会写路由器的加密逻辑，现在需要人工输入加密后的密码，将会在最近更新自动登录功能**


程序中需要自行改动的地方已标出。

![Image text](https://github.com/xingyi122/Anti_Mentor/blob/main/photo/readme-photo1.png)
1. 路由器管理页登录ip，一般是192.168.0.1或者192.168.1.1。
      首先你需要：a）打开tplogin.cn，进入tplink管理员登录页面，输入密码，登录成功，确保你的密码是正确的。
               b）访问http://192.168.1.1 和http://192.168.0.1， 输入你的密码，跳转成功的页面即为对应的路由器管理页面ip，将正确的ip填到程序里。

2. 找到加密后的密码：
       在登陆之前按F12开启开发者模式，点击登录后，去network->all->name下面找到tplogin.cn,即可获得对应加密后的密码，将对应的加密后的密码复制到程序中修改。
![Image text](https://github.com/xingyi122/Anti_Mentor/blob/main/photo/readme-photo2.png)

3.你要监控的设备的mac地址
    进入登录页面后，点击设备管理，找到你要监控的设备之后点击管理，记录此处的mac地址，复制到程序中：
![Image text](https://github.com/xingyi122/Anti_Mentor/blob/main/photo/readme-photo3.png)

#运行代码：

  Win+r打开“运行”对话框
  cd  *****(你的webcam_alert.py所在的目录）
  python webcam_alert.py
![Image text](https://github.com/xingyi122/Anti_Mentor/blob/main/photo/readme-photo4.png)
  然后就大功告成啦！！！！

#TODO： 
自动化登录（填充账号密码），使用selenium模拟浏览器实现  
模拟浏览器的安装参考[https://www.cnblogs.com/lfri/p/10542797.html](https://www.cnblogs.com/lfri/p/10542797.html)
