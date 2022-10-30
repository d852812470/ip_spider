# coding=utf-8
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from queue import Queue
import threading
import os
import sys


class Kip_spider(object):

    def __init__(self, thread_count, pages):
        self._ua = UserAgent()
        self._headers = {
            "User-Agent": self._ua.random
        }
        self._thread_count = thread_count
        self._page = pages
        self._ip_list = []
        self._queue = Queue()
        self._threads = []
        self._total_count = 0

    def _get_url_p(self):
        if os.path.exists("./cache/urladdress.txt"):
            os.remove("./cache/urladdress.txt")
        for p in range(1, self._page + 1):
            url_p = f"https://www.kuaidaili.com/free/inha/{p}/"
            with open("./cache/urladdress.txt", "a+") as f:
                f.write(url_p + "\n")

    def _init_queue(self):
        with open("./cache/urladdress.txt", "r") as f:
            for u in f:
                self._queue.put(u.rstrip())
        self._total_count = self._queue.qsize()

    def start(self):
        self._get_url_p()
        self._init_queue()
        for i in range(self._thread_count):
            self._threads.append(self.Spider_run(self._headers, self._queue, self._ip_list, self._total_count))
        for i in self._threads:
            i.start()
            time.sleep(1.5)
        for i in self._threads:
            i.join()
        self._ip_list = list(set(self._ip_list))
        if os.path.exists(f"./ip_cache/kuai_ip.txt"):
            os.remove(f"./ip_cache/kuai_ip.txt")
        with open(f"./ip_cache/kuai_ip.txt", "a+") as f:
            for i in self._ip_list:
                f.write(i + "\n")
        sys.stdout.write("\n")
        print("文件写入完成！！")

    class Spider_run(threading.Thread):
        def __init__(self, headers, queue, ip_list, total_count):
            super().__init__()
            self._headers = headers
            self._queue = queue
            self._ip_list = ip_list
            self._total_count = total_count

        def run(self):
            while not self._queue.empty():
                time.sleep(1)
                response = requests.get(self._queue.get(), headers=self._headers)
                self._msg(self._queue.qsize())
                if response.status_code == 200:
                    html = response.text
                    response.close()
                    soup = BeautifulSoup(html, "lxml")
                    tbody = soup.find("tbody")
                    trs = tbody.find_all("tr")
                    for tr in trs:
                        tds = tr.find_all("td")
                        ip = tds[0].text
                        port = tds[1].text
                        ip_port = ip + ":" + port
                        url_proxy = 'http://httpbin.org/ip'
                        proxy = {
                            "http": f"http://{ip_port}",
                            "https": f"http://{ip_port}"
                        }
                        try:
                            response = requests.get(url_proxy, proxies=proxy, timeout=2)
                            res_str = response.text
                            if ip in res_str:
                                self._ip_list.append(ip_port)
                        except Exception as e:
                            pass

        def _msg(self, last_count):
            """
            进度条
            :return:
            """
            last = round((last_count / self._total_count) * 100, 3)
            already_do = round(100 - last, 3)
            sys.stdout.write(f"\r已经完成了{already_do}%,还剩{last}%")
