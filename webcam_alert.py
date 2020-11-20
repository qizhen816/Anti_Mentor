import json
import re
import time
import requests
import random
import webbrowser
from bs4 import BeautifulSoup

# 路由器管理页登录ip,需要确认
url = 'http://192.168.1.1'
# 路由器设备控制页面ip
url_s = 'http://192.168.1.1/cgi-bin#/pc/deviceManage'
# 加密后的密码，需自行修改
pwd = "o1T3EXQ%2FZ44WZebcXbfHb%2BVbzmvM3WqH3EmJwJ%2FBh3M%2BISZSeKBe6yXMf6OI4oOglglSghzUxYtSi%2Fmvfy3f%2BOVkgJdTlaIKocS0pU8cyFZDWZuikoQoaK8Kw7XWxd9u2v7PGdEpVP1ajapolS%2BzRFFQTgpGBEIPid3hKV8MVic%3D"
# 路由器设备控制页面的摄像头的mac地址，需自行修改
dev_name = "SXT"
# 上传速度阈值 KB/s
limit = 10
# 学术页面，在检测到摄像头打开时开启，随机抽取列表中的一个
web = ['http://www.baidu.com',
       'https://github.com/YangZhongy/TrafficLights_control_pytorch_rl',
       'https://zhuanlan.zhihu.com/p/21421729',
       'https://www.coursera.org/browse?source=deprecated_spark_cdp',
       'https://blog.csdn.net/yeqiang19910412/article/details/76468407']

''' TODO 使用selenium模拟登陆
pwd = '你的路由器密码'
# selenium设置的driver名称
driver_path = "chromedriver.exe"

def login():
    from selenium.webdriver.chrome.options import Options
    from selenium import webdriver

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    #
    browser.get(url_dhcpclient)
    sp(5)
    browser.find_element_by_id('lgPwd').send_keys(MIMA)
    browser.find_element_by_id('loginSub').click()
    sp(2)
    browser.get(url_dhcpclient)
    sp(600)
    browser.find_element_by_id('routeMgtMbtn').click()
    sp(3)
    return browser
    
'''


headers1 = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Length': '39',
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': url[6:],
    'Origin': url,
    'Proxy-Connection': 'keep-alive',
    'Referer': url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

payload = json.dumps({
    "method": "do",
    "login": {"encrypt_type": 1,
              "password": pwd
              }})


def login_old():
    return requests.post(url, data=payload, headers=headers1)


def sp(int):
    time.sleep(int)

def get_all_host(r):
    # stok = r.get('stok')
    stok = re.findall('stok":".*?"', r, re.S)[0][7:-1]
    payload = json.dumps({"hosts_info": {"table": "host_info"}, "method": "get"})
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Length': '54',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': '192.168.1.1',
        'Origin': url,
        'Proxy-Connection': 'keep-alive',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    url_ = url + '/stok=' + stok + '/ds'
    response = requests.post(url_, data=payload, headers=headers)
    return response.text


def getUpSpeedBS(browser, safe):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    items = soup.select('#eptMngList')[0].find_all('div', {"class": "eptCon"})
    for item in items:
        if (item.find('span', {'class': 'name'}).get_text().strip() == dev_name):
            pp = item.find('p', {'class': 'vs'}).get_text()
            su = pp.split("上行")[1].split("下行")[0]
            sd = pp.split("上行")[1].split("下行")[1]
            print(time.asctime(time.localtime(time.time())), '上传', su, '下载', sd)
            if su[-4] == 'M' or sd[-4] == 'M':
                if safe == True:
                    webbrowser.open(web[int(random.uniform(0, 4))])
                    safe = False
            else:
                if (su[-4] == 'K' and int(su.split('K')[0]) >= limit) or (
                        sd[-4] == 'K' and int(sd.split('K')[0]) >= limit):
                    if safe == True:
                        webbrowser.open(web[int(random.uniform(0, 4))])
                        safe = False
                else:
                    safe = True
    return safe


def getUpSpeed(rr, safe):
    hosts = re.findall('mac":.*?hostname', rr, re.S)
    for j in hosts:
        if j.find('78-11-DC-D6-9F-5F') != -1:
            speed = re.findall('"up_speed":"\d+"', j)[0]
            speed = int(re.findall(r'\d+', speed)[0]) / 1024
            print(time.asctime(time.localtime(time.time())), speed, 'kB/s')
            if speed > 10 and safe == True:
                webbrowser.open(web[int(random.uniform(0, 4))])
                safe = False
            if speed < 10 and safe == False:
                safe = True
    return safe


def newLog(t):
    page = login_old()
    print(page)
    safe = True
    # 这里的50000是个阈值，程序开启的时长
    while time.time() - t < 50000 or safe == False:
        rr = get_all_host(page.text)
        safe = getUpSpeed(rr, safe)
        time.sleep(0.1)


if __name__ == '__main__':
    newLog(time.time())
