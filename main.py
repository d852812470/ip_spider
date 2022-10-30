# coding=utf-8
from optparse import OptionParser
from kuai_spider import Kip_spider
from spider import Ip_spider
import sys

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-m", "--mode", dest="mode", type="int", default=1,
                      help="爬取模式(1 or 2)", metavar="NUMBER")
    parser.add_option("-t", "--thread", dest="thread", type="int", default=10,
                      help="线程数目", metavar="NUMBER")
    parser.add_option("-p", "--page",
                      type="int", dest="page",
                      help="第二种模式下需要爬取的页数，如果是第一种就不需要设置", metavar="NUMBER")
    (options, args) = parser.parse_args()
    if len(sys.argv) == 7 and int(sys.argv[2]) == 2:
        kuai_spider = Kip_spider(int(sys.argv[4]), int(sys.argv[6]))
        kuai_spider.start()
    elif len(sys.argv) == 5 and int(sys.argv[2]) == 1:
        ip_spider = Ip_spider(int(sys.argv[4]))
        ip_spider.start()
    else:
        print("请输入正确参数")
        parser.print_help()
