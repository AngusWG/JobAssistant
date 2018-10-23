import os
import sys

import pymongo

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace("\\", "/", 100)
rootsub = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/", 100)
sys.path.append(root)
sys.path.append(rootsub)
import requests
from pyquery import PyQuery as pq
import threading
# from ldzhuaqu.db.SqlFactory import SqlFactory
import time


class 代理ip池:

    def __init__(self):
        self.ip代理池 = set()

    def main(self):
        try:
            print("正在启动ip数据获取")
            one = threading.Thread(target=self.ipGetData, args=(1,))
            one.start()
            # self.ipGetData(1)
        except Exception as e:
            print("Error: 无法启动线程")
        pass

    def ipGetData(self, num):
        print("ip数据获取启动成功")
        ip代理池 = self.ip代理池
        while True:
            try:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "max-age=0",
                    "If-None-Match": 'W/"8af0b700956e4c37b5fd98c27260de46"',
                    "Host": "www.xicidaili.com", "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                }
                rep = requests.get("http://www.xicidaili.com/nn", headers=headers)
                if rep.status_code == 200:
                    p = pq(rep.text)
                    trs = p("#ip_list").find("tr")
                    for tr in trs:
                        try:
                            tds = p(tr).find("td")
                            if len(tds) > 6:
                                ip = p(tds[1]).text().replace(" ", "")
                                port = p(tds[2]).text().replace(" ", "")
                                ifgn = p(tds[5]).text().replace(" ", "")
                                resultip = self.yanZhengIp(ip + ":" + port, ifgn)
                                if resultip == "" or resultip == '':
                                    continue
                                else:
                                    ip代理池.add("{}://{}:{}".format(ifgn.lower(), ip, port))
                                    # print("获取ip：" + ip + ":" + port + "数据成功")
                        except Exception as e:
                            print(e)
                            pass
            except Exception as e:
                print(e)
                pass
            while len(ip代理池) >= 20:
                print("ip池里有{} 休息一下".format(len(ip代理池)))
                time.sleep(60 * 3)
        pass

    @staticmethod
    def yanZhengIp(ip, type):
        try:
            rep = None
            if type == "http" or type == "HTTP":
                rep = requests.get('http://www.baidu.com', proxies={"http": "http://" + ip}, timeout=1)
                return ip
            else:
                rep = requests.get('http://www.baidu.com', proxies={"https": "https://" + ip}, timeout=1)
            if rep.status_code == 200:
                return ip
        except Exception as e:
            pass
        return ""


if __name__ == "__main__":
    c = 代理ip池()
    c.main()
