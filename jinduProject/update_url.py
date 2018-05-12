#更新链接
#1 如果网站无规律更新 定时重新爬取所有链接
#2 定时获取每个分类的首页内容，与以前的内容对
import sqlite3
con = sqlite3.connect("/home/zuofeng/jindu.db")
cur = con.cursor()
cur.execute("""
    CREATE TABLE `urls` (
	`url`	TEXT UNIQUE,
	`flag`	INTEGER,
	`error`	INTEGER,
	`content`	TEXT,
	PRIMARY KEY(url)
);
""")
con.commit()
con.close()