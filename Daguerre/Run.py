# encoding: utf-8
__author__ = 'lianggao'
__date__ = '2018/5/11 上午11:27'

from scrapy import cmdline


def main():
    cmdline.execute("scrapy crawl superspider".split())


if __name__ == '__main__':
    main()