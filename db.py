import pymysql.cursors
con = pymysql.connect(host='localhost',
                      user='root',
                      password='',
                      database='sms'
                      )
cursor = con.cursor()


# sample=[]
# sql="select * from timetable"
# cursor.execute(sql)
# var = cursor.fetchall()
# for i in var:
#     sample.append(i)

# a=sample[0]
# b=sample[1]
# c=sample[3]
# d=sample[4]
# e=sample[5]
# f=sample[6]
# g=sample[7]
# data=[a,b,c,d,e,f,g]

# print(a)
sql="alter table students modify id varchar(220)"
cursor.execute(sql)
con.commit()












































# sql = '''create table `students`(
# `id` int(100),
# `name` varchar(200),
# `email` varchar(50),
# `phone` varchar(50),
# `gender` varchar(10),
# `year` int(10),
# `sem` int(10),
# `section` varchar(10),
# `branch` varchar(20),
# `attendance` int(200),

# primary key(id)
# )'''



# sql = '''create table `faculty`(
# `fid` int(200),
# `name` varchar(200),
# `email` varchar(200),
# `password` varchar(200)
#  `subject` varchar(230)
# )'''


# sql='''create table `timetable`(
# `periods` varchar(220),
# `monday` varchar(220),
# `tuesday` varchar(220),
# `wednesday` varchar(220),
# `thursday` varchar(220),
# `friday` varchar(220),
# `saturday` varchar(220)
# )'''