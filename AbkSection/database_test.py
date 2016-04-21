#coding=utf-8
import MySQLdb

conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='database',
        db ='test',
        )
cur = conn.cursor()

#创建数据表
#cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")

#插入一条数据
cur.execute("insert into Myclass values(5,'Tom')")

#插入一条数据
sqli="insert into student values(%s,%s,%s,%s)"
cur.execute(sqli,('3','Huhu','2 year 1 class','7'))

#一次插入多条记录
sqli="insert into student values(%s,%s,%s,%s)"
cur.executemany(sqli,[
        ('3','Tom','1 year 1 class','6'),
   		('3','Jack','2 year 1 class','7'),
    	('3','Yaheng','2 year 2 class','7'),
    ])

#获得表中有多少条数据
aa=cur.execute("select * from student")
print aa

#打印表中的多少数据
info = cur.fetchmany(aa)
for ii in info:
    print ii

#修改查询条件的数据
#cur.execute("update student set class='3 year 1 class' where name = 'Tom'")

#删除查询条件的数据
#cur.execute("delete from student where age='9'")

cur.close()
conn.commit()
conn.close()
