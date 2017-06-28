# coding: utf-8

from spider import Spider

if __name__ == "__main__":
    import time
    print("Start At:",time.asctime( time.localtime(time.time()) ))
    spider = Spider()
    spider.start()
    print("Stop At:",time.asctime( time.localtime(time.time()) ))