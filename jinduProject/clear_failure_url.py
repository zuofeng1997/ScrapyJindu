#去掉失效链接

import sqlite3
con = sqlite3.connect('/home/zuofeng/jindu.db')
cur = con.cursor()

result = cur.execute("select url from urls where error>2")
for i in result:
    failure_url = i[0]
    cur.execute("delete from urls where url=%s" % "'" + failure_url + "'")

con.commit()
con.close()