# Anti_Mentor
This is an honorable instrunction of automatically warning yourself when working fish in lab.

#如何在办公室反监控小米摄像头快乐摸鱼  
主要思路是模拟浏览器登录路由器管理网页→进入监控流量上传下载的子网页→找到摄像头ID→监控上传流量→发现异常报警，打开学术页面

*需要满足的条件*：TP-Link路由器，否则需要自行修改页面逻辑

**我爬虫太菜了，不会写路由器的加密逻辑，现在需要人工输入加密后的密码，将会在最近更新自动登录功能**

1. 登录路由器管理页面（一般是192.168.0.1或者192.168.1.1），F12开启开发者模式，定位到密码字段，输入密码，获得加密后的字符串

2. 修改[webcam_alert.py](webcam_alert.py)中的关键参数，详情看代码备注

3. 测试代码 `python webcam_alert.py`

#TODO： 
自动化登录（填充账号密码），使用selenium模拟浏览器实现  
模拟浏览器的安装参考[https://www.cnblogs.com/lfri/p/10542797.html](https://www.cnblogs.com/lfri/p/10542797.html)
