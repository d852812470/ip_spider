# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from queue import Queue
import threading
import os
import sys


class Ip_spider(object):
    def __init__(self, thread_count):
        self._base_url = "http://www.66ip.cn"
        self._ua = UserAgent()
        self._queue = Queue()
        self._thread_count = thread_count
        self._threads = []
        self._result = []
        self._total_count = 0

    def init_pages(self):
        """
        初始化我们需要爬取的地址
        :return:
        """
        # 先判断文件是否存在
        if os.path.exists("./cache/pages.log"):
            os.remove("./cache/pages.log")
        headers = {
            "User-Agent": self._ua.random
        }
        response = requests.get(self._base_url, headers=headers)
        html = response.content.decode("gb2312")
        # 将所有需要爬取的URL收集起来
        soup = BeautifulSoup(html, "lxml")
        a_list = soup.find_all(name="a", attrs={"href": re.compile("^/areaindex_")})
        for a in a_list:
            with open("./cache/pages.log", "a+") as f:
                f.write(self._base_url + a['href'] + "\n")

    def init_queue(self):
        """
        初始化队列： 将存放在cache中的需要爬取的url读取出来，然后放入队列中
        :return:
        """
        # 读日志
        with open("./cache/pages.log", "r") as f:
            for u in f:
                self._queue.put(u.rstrip())
        # 保存总的长度
        self._total_count = self._queue.qsize()

    def start(self):
        # 先初始化
        self.init_pages()
        self.init_queue()
        # 准备线程
        for i in range(self._thread_count):
            self._threads.append(self.Ip_spider_run(self._queue, self._ua, self._result, self._total_count))
        # 启动线程
        for t in self._threads:
            t.start()
        # 等待子线程结束
        for t in self._threads:
            t.join()
        # 处理总的结果
        self._result = list(set(self._result))
        if os.path.exists(f"./ip_cache/66_ip.txt"):
            os.remove(f"./ip_cache/66_ip.txt")
        with open(f"./ip_cache/66_ip.txt", "a+") as f:
            for i in self._result:
                f.write(i + "\n")
        sys.stdout.write("\n")
        print("文件写入完成！！")

    class Ip_spider_run(threading.Thread):
        """
        一个内部类： 这个专门
        """

        def __init__(self, queue, ua, result, total_count):
            super().__init__()
            self._queue = queue
            self._ua = ua
            self._result = result
            self._total_count = total_count  # 队列的总长度

        def msg(self):
            """
            显示进度
            :return:
            """
            last = round((self._queue.qsize() / self._total_count) * 100, 3)
            alreadly_do = round(100 - last, 3)
            sys.stdout.write(f"\r已经扫描：{alreadly_do}%, 还剩：{last}%")

        def run(self):
            """
            一个内部类： 这个专门用于跑线程
            :return:
            """
            while not self._queue.empty():
                headers = {
                    "User-Agent": self._ua.random
                }
                # print(self._queue.get())
                response = requests.get(self._queue.get(), headers=headers)
                # 显示进度
                self.msg()

                html = response.content.decode("gb2312")
                soup = BeautifulSoup(html, "lxml")
                table = soup.find("table", bordercolor="#6699ff")
                # 再找tr
                trs = table.find_all("tr")
                del (trs[0])
                for tr in trs:
                    tds = tr.find_all("td")
                    ip = tds[0].text
                    port = tds[1].text
                    ip_port = ip + ":" + port
                    # 验证ip是否可用
                    url_test_proxy = 'http://httpbin.org/ip'
                    proxy = {
                        "http": f"http://{ip_port}",
                        "https": f"http://{ip_port}"
                    }
                    # print(proxy)
                    try:
                        res = requests.get(url_test_proxy, proxies=proxy, timeout=2)
                        # 判断结果
                        res_str = res.text
                        if ip in res_str:
                            self._result.append(ip_port)
                    except Exception as e:
                        pass






