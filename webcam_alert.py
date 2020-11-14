import json
import re
import time
import requests
import base64
import webbrowser
import random
from bs4 import BeautifulSoup

MIMA = 'tang1981'
dev_name = "SXT"
url = 'http://192.168.1.1'
url_s = 'http://192.168.1.1/cgi-bin#/pc/deviceManage'
driver_path = "chromedriver.exe"
limit = 10

web = ['http://www.baidu.com',
       'https://github.com/YangZhongy/TrafficLights_control_pytorch_rl',
       'https://zhuanlan.zhihu.com/p/21421729',
       'https://www.coursera.org/browse?source=deprecated_spark_cdp',
       'https://blog.csdn.net/yeqiang19910412/article/details/76468407']

headers1 = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Length': '39',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': '192.168.1.1',
        'Origin': 'http://192.168.1.1',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.1.1/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

payload = json.dumps({
    "method": "do",
    "login":{"encrypt_type": 1,
             "password":
"o1T3EXQ%2FZ44WZebcXbfHb%2BVbzmvM3WqH3EmJwJ%2FBh3M%2BISZSeKBe6yXMf6OI4oOglglSghzUxYtSi%2Fmvfy3f%2BOVkgJdTlaIKocS0pU8cyFZDWZuikoQoaK8Kw7XWxd9u2v7PGdEpVP1ajapolS%2BzRFFQTgpGBEIPid3hKV8MVic%3D"

             }})

url_dhcpclient = 'http://192.168.1.1'

def login_old():
    return requests.post(url_dhcpclient,data=payload,headers=headers1)

def sp(int):
    time.sleep(int)

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
    browser.find_element_by_id('lgPwd').send_keys('tang1981')
    browser.find_element_by_id('loginSub').click()
    sp(2)
    browser.get(url_dhcpclient)
    sp(600)
    browser.find_element_by_id('routeMgtMbtn').click()
    sp(3)
    return browser


def get_all_host(r):
    # stok = r.get('stok')
    stok = re.findall('stok":".*?"',r, re.S)[0][7:-1]
    payload = json.dumps({"hosts_info":{"table":"host_info"},"method":"get"})
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Length': '54',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': '192.168.1.1',
        'Origin': 'http://192.168.1.1',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.1.1/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    url = 'http://192.168.1.1/stok='+stok+'/ds'
    response = requests.post(url, data=payload, headers=headers)
    return response.text

#78-11-DC-D6-9F-5F
#48-8A-D2-49-40-EA

def getUpSpeedBS(browser,safe):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    items = soup.select('#eptMngList')[0].find_all('div', {"class": "eptCon"})
    for item in items:
        if (item.find('span', {'class': 'name'}).get_text().strip() == dev_name):
            pp = item.find('p', {'class': 'vs'}).get_text()
            su = pp.split("上行")[1].split("下行")[0]
            sd = pp.split("上行")[1].split("下行")[1]
            print(time.asctime(time.localtime(time.time())),'上传',su,'下载',sd)
            if su[-4] == 'M' or sd[-4] == 'M':
                if safe == True:
                    webbrowser.open(web[int(random.uniform(0,4))])
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

def getUpSpeed(rr,safe):

    hosts = re.findall('mac":.*?hostname',rr, re.S)
    for j in hosts:
        if j.find('78-11-DC-D6-9F-5F')!=-1:
            speed = re.findall('"up_speed":"\d+"',j)[0]
            speed = int(re.findall(r'\d+',speed)[0])/1024
            print(time.asctime(time.localtime(time.time()) ),speed,'kB/s')
            if speed > 10 and safe == True:
                webbrowser.open(web[int(random.uniform(0,4))])
                safe = False
            if speed < 10 and safe == False:
                safe = True
    return safe


def newLog(t):
    page = login_old()
    print(page)
    safe = True
    while time.time() - t < 50000 or safe == False:
        rr = get_all_host(page.text)
        safe = getUpSpeed(rr,safe)
        time.sleep(0.1)

def main():
    newLog(time.time())


main()
