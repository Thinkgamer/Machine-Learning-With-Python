# coding: utf-8

from bs4 import BeautifulSoup
import urllib2
import urllib
import time,os

class Spider:

    def __init__(self):
        self.search_url = 'https://tieba.baidu.com/f?kw='
        self.tieba_list = []      # 存储要爬取的若干个贴吧的链接
        self.url_list = []        # 存放每个贴吧前三页的帖子链接
        self.timesleep = 2        # 每次访问tieba的url时间间隔
        self.pages = 3            # 设置要抓取多少页
        self.current_href = ''    # 当前爬取的贴吧链接url

        # 在data目录下创建日期和贴吧名的txt文件
        if not os.path.exists('data/%s' % time.strftime('%Y%m%d')):
            os.mkdir('data/%s' % time.strftime('%Y%m%d'))

    def error(self,loc,url,e):
        fw = open("error/error.log","a")
        fw.write(time.asctime( time.localtime(time.time()) )+"\t"+loc+"\t"+url+"\t"+str(e))
        fw.close()

    # 模拟浏览器进行登录
    def get_page(self,href):
        res = urllib2.urlopen(href)
        # 如果访问成功的话返回读取的内容，否则返回空的字符串
        if res.code == 200:
            return res.read()
        else:
            return ""

        # 从文件中加载贴吧名并组成url
    def read(self):
        try:
            with open("tiebaname/name.txt", "r") as fr:
                for line in fr.readlines():
                    # urllib.quote(line.strip()) 将关键字转变成url 格式
                    self.tieba_list.append(self.search_url + urllib.quote(line.strip()) + "&ie=utf-8&pn=")
            fr.close()
        except Exception as e:
            self.error("read", "read error", e)
            pass
        finally:
            return self.tieba_list


    # 解析每个帖子共有几页
    def get_num(self,url):
        try:
            if self.get_page(url):
                body = BeautifulSoup(self.get_page(url), "html.parser")
                num_li = body.find_all("li", class_="l_reply_num", style="margin-left:8px")[0]
                num = num_li.findAll('span', class_='red')[1].get_text()
                # print(num)
                return int(num)
            else:
                pass
        except Exception as e:
            self.error("get_num",url,e)
            return 1

    # 解析每一个贴吧前三页的所有帖子连接
    def parse_href(self,one_tieba_url):
        self.url_list = []  # 存放一个贴吧前三页所有帖子的链接
        try:
            for i in range(0,self.pages):
                url = one_tieba_url + str(i * 50)
                try:
                    # i* 50 控制翻页，每页显示50个
                    if self.get_page(one_tieba_url+str(i*50)):
                        body = BeautifulSoup(self.get_page(url), "html.parser")
                        div_list = body.find_all("div", class_="threadlist_title pull_left j_th_tit ")  # 解析到每一个帖子
                        for div in div_list:
                            # print(div.a.get('href'),div.a.get_text())
                            # print("https://tieba.baidu.com" + div.a.get('href'))
                            self.url_list.append("https://tieba.baidu.com" + div.a.get('href'))
                    else:
                        pass
                except Exception as e:
                    self.error("parse_href",url,e)
                    pass
                # time.sleep(self.timesleep)
        except Exception as e:
            self.error("parse_href",one_tieba_url,e)
            pass

    # 解析每个贴吧前三页所有帖子的发帖人和回帖人的用户名
    def parse_username(self):
        try:
            # 解析每个帖子对应的发帖人和回帖人
            for url in self.url_list:
                filename = urllib.unquote(self.current_href.split("kw=")[1].split("&ie=")[0])              # 贴吧名字，也是文件名
                fw = open('data/%s/%s.txt' % (time.strftime('%Y%m%d'), filename), 'a')

                try:
                    fw.write(url+"\t")
                    num = self.get_num(url)
                    for i in range(1,num+1):
                        one_url = url+"?pn="+str(i)   # https://tieba.baidu.com/p/5183701449?pn=1
                        # print("total %s papges, now parse is %s page，url is：%s"%(num,i,one_url))
                        # 解析用户名
                        if self.get_page(one_url):
                            li_list = BeautifulSoup(self.get_page(one_url), "html.parser").find_all('li',class_='d_name')
                            for li in li_list:
                                # print(li.a.get_text())
                                fw.write(li.a.get_text().encode("utf-8")+"\t")
                            # time.sleep(self.timesleep)
                        else:
                            pass
                    fw.write("\n")
                    fw.close()
                    print(url)
                except Exception as e:
                    self.error("parse_username",url,e)
                    pass

                time.sleep(self.timesleep)
        except Exception as e:
            self.error("parse_username",url,e)
            pass

    def start(self):
        self.read()  # load tieba_prepare name
        for url in self.tieba_list:
            try:
                self.current_href =url
                print("Start:",self.current_href,time.strftime("%Y-%m-%d %H-%M-%S")) #self.current_href,
                self.parse_href(url)  # 解析该贴吧对应的前三页的每个帖子的链接
                self.parse_username() # 解析每个帖子的发帖人和回帖人
            except Exception as e:
                self.error("start","parse error at start",e)
                pass

            time.sleep(self.timesleep)
            print("Over:",time.strftime("%Y-%m-%d %H-%M-%S"))