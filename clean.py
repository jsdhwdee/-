import csv
import re
import psycopg2

def openfile(site):
    line_list = []
    with open(site, "r", encoding='utf-8')as f:
        s = csv.reader(f)
        for i in s:
            line_list.append(i)
    return line_list

def change(b):
    a = [""]*11
    a[0] = "汽车零配件"  # 行业
    a[1] = b[0]  # 职位
    a[2] = b[1]  # 公司
    a[3] = b[2]  # 位置
    if "-" in b[3]:
        if "万/年" in b[3]:
            idx1 = b[3].index('-')  # 定位 "-" 的位置
            idx2 = b[3].index('万')  # 定位到 "万" 的位置
            x = 10000
            max = float(b[3][0:idx1]) * x  # 薪资上限
            min = float(b[3][idx1 + 1:idx2]) * x  # 薪资下限
            a[4] = str((min+max)/24)  # 每月平均工资
        elif "千/月" in b[3]:
            idx1 = b[3].index('-')
            idx2 = b[3].index('千')
            x = 1000
            max = float(b[3][0:idx1]) * x  # 薪资上限
            min = float(b[3][idx1 + 1:idx2]) * x  # 薪资下限
            a[4] = str((min + max) * 0.5)
        elif "万/月" in b[3]:
            idx1 = b[3].index('-')
            idx2 = b[3].index('万')
            x = 10000
            max = float(b[3][0:idx1]) * x  # 薪资上限
            min = float(b[3][idx1 + 1:idx2]) * x  # 薪资下限
            a[4] = str((min + max) * 0.5)
        else:
            print(b[3])
    else:
        if "元/天" in b[3]:
            idx = b[3].index('元')  # 定位到 "万" 的位置
            x = 20
            a[4] = str(float(b[3][0:idx]) * x)  # 薪资
        elif "元/小时" in b[3]:
            idx = b[3].index('元')
            x = 160
            a[4] = str(float(b[3][0:idx]) * x)  # 薪资
        else:
            print(b[3])
    a[5] = b[4]  # 发布时间
    try:  # 学历要求
        a[6] = b[5].split('|')[0].split('：')[1]
    except:
        a[6] = ""
    try:  # 工作经验
        a[7] = b[5].split('|')[1].split('：')[1]
    except:
        a[7] = ""
    try:  # 公司性质
        a[8] = b[5].split('|')[2].split('：')[1]
    except:
        a[8] = ""
    try:  # 公司规模
        a[9] = b[5].split('|')[3].split('：')[1]
    except:
        a[9] = ""
    a[10] = b[6]  # 具体要求
    return a

def putresult():
    site = "65.csv"
    file = openfile(site)  # 读取一个csv
    for line in file:
        if line[3] and "以上" not in line[3] and "以下" not in line[3]:
            result = change(line)
            # print(result)
            with open('data.csv', 'a+', encoding='utf-8-sig') as f:
                f.write(result[0] + ',' + result[1] + ',' + result[2] + ',' + result[3] + ',' + result[4] + ',' +
                        result[5] + ',' + result[6] + ',' + result[7] + ',' + result[8] + ',' + result[9] + ',' +
                        result[10] + '\n')
            # insert(tuple(result), "forecast")


putresult()