# coding=utf-8
from optparse import OptionParser
from kuai_spider import Kip_spider
from spider import Ip_spider
import sys

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-m", "--mode", dest="mode", type="int", default=1,
                      help="type of spider", metavar="NUMBER")
    parser.add_option("-t", "--thread", dest="thread", type="int", default=10,
                      help="the count num of thread", metavar="NUMBER")
    parser.add_option("-p", "--page",
                      type="int", dest="page",
                      help="if mode=2 the page of scan", metavar="NUMBER")
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
