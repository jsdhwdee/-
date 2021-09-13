import time
import requests
from bs4 import BeautifulSoup
import os
import csv

# 构建请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}

url_pattern = "https://jobs.51job.com/{}/hy{}/p{}/"
cities = ['ningbo', 'chongqin', 'xian', 'suzhou', 'wuhan', 'nanjing', 'tianjing', 'zhengzhou', 'changsha', 'dongguan', 'foshan', 'qingdao', 'shenyang']

# for city in cities:
#     if not os.path.exists(city+".csv"):
#         # 创建存储csv文件存储数据
#         file = open(city+'.csv', "w", encoding="utf-8-sig", newline='')
#         csv_head = csv.writer(file)
#         # 表头
#         header = ['trade', 'job', 'company', 'place', 'salary', 'date', 'education', 'experience', 'scale', 'detail']
#         csv_head.writerow(header)
#         file.close()

for city in cities:
    for trade in range(1, 66):
        if trade < 10:
            trade = "0"+str(trade)
        for page in range(1, 51):
            # 增加时延防止反爬虫
            time.sleep(5)
            url = url_pattern.format(city, trade, page)
            print(url)
            response = requests.get(url=url, headers=headers)
            # 声明网页编码方式，需要根据具体网页响应情况
            response.encoding = 'gbk'
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # 解析
            for i in soup.find('div', class_='detlist gbox').find_all('div'):
                time.sleep(3)
                job = i.find('p', class_='info').find('span', class_='title').a['title']
                print("job:", job)
                if i.find('p', class_='info').find('a', class_='name').get_text():
                    company = i.find('p', class_='info').find('a', class_='name').get_text()
                else:
                    company = ""
                print("company", company)
                if i.find('p', class_='info').find('span', class_="location name").get_text():
                    place = i.find('p', class_='info').find('span', class_="location name").get_text()
                else:
                    place = ""
                print("place", place)
                if i.find('p', class_='info').find_all('span', class_="location")[1].get_text():
                    salary = i.find('p', class_='info').find_all('span', class_="location")[1].get_text()
                else:
                    salary = ""
                print("salary", salary)
                if i.find('p', class_='info').find('span', class_='time').get_text():
                    date = i.find('p', class_='info').find('span', class_='time').get_text()
                else:
                    date = ""
                print("date", date)
                if i.find('p', class_='order').get_text():
                    need = i.find('p', class_='order').get_text()
                education = need.split('|')[0]
                print("学历要求", education)
                experience = need.split('|')[1]
                print("经验要求", experience)
                scale = need.split('|')[2]
                print("公司性质", scale)
                if i.find('p', class_='text').get_text():
                    detail = '"' + i.find('p', class_='text').get_text() + '"'
                else:
                    detail = ""
                print("detail", detail)
                with open(city+'.csv', 'a+', encoding='utf-8-sig') as f:
                    f.write(trade + ',' + job + ',' + company + ',' + place + ',' + salary + ',' + date + ',' + education + ',' + experience + ',' + scale + ',' + detail + '\n')