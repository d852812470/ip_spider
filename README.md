# ip代理池扫描
##### 下载代码:
* git clone

```bash
git clone https://github.com/d852812470/ip_spider.git
```
##### 安装依赖:

```bash
pip install requests,bs4,fake_useragent,queue
```
支持https://www.kuaidaili.com/free/  和  http://www.66ip.cn/ 扫描  
##### 参数:

* -m  
模式：1或者2，1为66ip，2为快代理
* -t  
线程数目
* -p  
爬取的页数，模式为2时需要设置，不建议设置太大，后面的页数已经很久没有验证了  

##### 文件写入位置在ip_cache

执行python main.py查看帮助  
