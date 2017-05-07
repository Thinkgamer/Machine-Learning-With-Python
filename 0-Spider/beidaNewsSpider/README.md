爬取北大要闻的所有新闻

url:http://pkunews.pku.edu.cn/xxfz/node_185.htm

news.sql 为数据备份（Mysql）

数据库文件备份与恢复
备份：/usr/bin/mysqldump -uroot -proot beidaspider  --default-character-set=utf8 --opt -Q -R >./news.sql
恢复：/usr/bin/mysql -uroot -proot beidaspider <./news.sql
