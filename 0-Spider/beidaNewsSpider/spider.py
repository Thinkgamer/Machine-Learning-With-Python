# coding: utf-8

import pymysql
from bs4 import BeautifulSoup
import urllib.request
import time

'''
创建数据库和数据表语句
create database beidaspider default charset utf8;

create table news(
title  varchar(100),
pub_date date,
from_ varchar(50),
content varchar(20000)
);

数据库备份
/usr/bin/mysqldump -uroot -proot beidaspider  --default-character-set=utf8 --opt -Q -R >./news.sql

数据库恢复
/usr/bin/mysql -uroot -proot beidaspider <./news.sql
'''


class BeiDaSpider:
    # 初始化
    def __init__(self):
        self.root_href = "http://pkunews.pku.edu.cn/xxfz/"

    # 连接数据库
    def connMysql(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root',db='beidaspider',charset='utf8')
        cur = conn.cursor()
        return cur,conn

    # 写入数据库
    def write(self,title,date,from_,content):
        cur,conn = self.connMysql()
        sql = """INSERT INTO news (title, pub_date, from_, content) VALUES ("%s", "%s", "%s", "%s")""" % (title,date,from_,content)
        cur.execute(sql)
        conn.commit()
        conn.close()

        with open("news.txt","a") as fp:
            fp.write(title+"\t"+date+"\t"+from_+"\t"+content+"\n")
        fp.close()

    # 解析每页，获取该页所有的新闻链接
    def parse_onePage_href(self,url):
        res = urllib.request.urlopen(url)
        body = BeautifulSoup(res.read())
        table = body.find('table',cellspacing="0",cellpadding="0",id="nav2_7Tabcontent_10")
        a_list = table.find_all('a')
        href_list = []
        for a in a_list:
            href_list.append(self.root_href + a.get('href'))
        return href_list

    # 解析每个新闻，获取数据
    def parse_oneNew(self,url):
        res = urllib.request.urlopen(url)
        body = BeautifulSoup(res.read())

        # 获取标题
        title = body.title.get_text().strip()
        print(title)

        # 获取时间和来源
        #dataAndfrom =
        dataAndfrom = body.find('table',width="560",border="0",cellspacing="0",cellpadding="0")
        datafrom_list = dataAndfrom.find_all('tr')[0].get_text().strip().split("  ")
        date = datafrom_list[0].split("：")[1].strip()
        from_ = datafrom_list[1].split("：")[1].strip()
        print(date)
        #print(from_)

        # 获取新闻内容
        content = body.find('table',width="710",border="0",cellspacing="0",cellpadding="0",style="margin-left:15px;").find_all('tr')[3].get_text().strip().replace("\n"," ")
        #print(content)

        self.write(title,date,from_,content)

    def start(self):
        for i in range(1,21):
            if i==1:
                href_list = self.parse_onePage_href(self.root_href + "node_185.htm")
                for href in href_list:
                    try:
                        self.parse_oneNew(href)
                    except Exception as e:
                        print(e)
                    finally:
                        pass
            #        time.sleep(1)
                    # break
            else:
                href_list = self.parse_onePage_href(self.root_href + "node_185_" + str(i) + ".htm")
                for href in href_list:
                    try:
                        self.parse_oneNew(href)
                    except Exception as e:
                        print(e)
                    finally:
                        pass
            #        time.sleep(1)
            #time.sleep(2)
            # break


if __name__=="__main__":
    spi = BeiDaSpider()
    spi.start()
