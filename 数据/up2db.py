import csv
import pymysql

def openfile(site):
    line_list = []
    csv.field_size_limit(500 * 1024 * 1024)
    with open(site, "r", encoding='utf-8')as f:
        s = csv.reader(f)
        for i in s:
            line_list.append(i)
    return line_list

def create():
    site = "CREATE TABLE xmdata(id int primary key,trade varchar(100),job varchar(100),company varchar(100)," \
           "place varchar(100),salary varchar(100),pubdate varchar(100),degree varchar(100),experience varchar(100)," \
           "nature varchar(100),scale varchar(100),detail varchar(5000))"
    site1 = "DROP TABLE IF EXISTS xmdata"
    # 连接
    db = pymysql.connect(database="tmt", user="root", password="123456", host="localhost", port=3306)
    # 创建一个游标
    cur = db.cursor()
    # 表已有则删除
    cur.execute(site1)
    # 创建表
    cur.execute(site)
    db.commit()  # 提交事务
    db.close()  # 关闭数据库

# 插入数据
def insert(value, name):
    # 连接数据库
    site = "INSERT INTO " + name + "(id,trade,job,company,place,salary,pubdate,degree,experience,nature,scale,detail)" \
                                   "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    db = pymysql.connect(database="tmt", user="root", password="123456", host="localhost", port=3306)
    cur = db.cursor()
    try:
        cur.execute(site, value)
        db.commit()
        print("插入成功！")
    except:
        db.rollback()
        print("插入失败！")
    db.close()

def change(k, b):
    a = [""]*12
    a[0] = k  # 序列
    a[1] = b[0]  # 行业
    a[2] = b[1]  # 工作
    a[3] = b[2]  # 公司
    a[4] = b[3]  # 位置
    a[5] = b[4]  # 薪资
    a[6] = b[5]  # 发布时间
    a[7] = b[6]  # 学历要求
    a[8] = b[7]  # 工作经验
    a[9] = b[8]  # 公司性质
    a[10] = b[9]  # 公司规模
    a[11] = b[10]  # 具体要求
    return a

def putresult():
    site = "data.csv"
    file = openfile(site)  # 读取
    k = 26351
    for line in file[26351:29359]:
        result = change(k, line)
        # print(result)
        insert(tuple(result), "xmdata")
        k = k+1


# create()
putresult()